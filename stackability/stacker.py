import stackability.datatypes as dt
import stackability.factories.sx as sx
import stackability.factories.gt as gt

class NonHomogeneousDeliveryException(Exception):
    pass



def _get_factory(trailer : dt.Trailer):
    return trailer.factory_name()
    

class Stacker:
    trailers : list[dt.Trailer]
    factory : str
    valid_lorries : list[dt.Lorry]

    def __init__(self, trailers : list[dt.Trailer]):
        factory = None
        for trailer in trailers:
                if factory is None:
                    factory = _get_factory(trailer)
                else:
                    if factory != _get_factory(trailer):
                        raise NonHomogeneousDeliveryException('Not all trailers are from same factory')
                
        self.factory = factory
        self.trailers = trailers
        if self.factory == 'SX':
            self.valid_lorries = sx.valid_lorries
        elif self.factory == 'GT':
            self.valid_lorries = gt.valid_lorries
        else:
            raise Exception(f'Invalid factory: {self.factory}')


    def remove_at(lst, indices):
        new_lst = []
        for idx, el in enumerate(lst):
            if idx not in indices:
                new_lst.append(el)

        return new_lst

    def pack_contained_trailers_greedy(trailers: list[dt.Trailer]) -> list[dt.Trailer]:
        remaining = trailers.copy()

        containers = [
            trailer for trailer in remaining
            if "VT3" in trailer.model_category() or "VT4" in trailer.model_category()
        ]

        # Fill larger container trailers first
        containers.sort(
            key=lambda trailer: (
                trailer.length or 0,
                trailer.width or 0,
                trailer.height or 0,
            ),
            reverse=True,
        )

        for container in containers:
            if container.contained_trailer is not None:
                continue

            candidates = []

            for candidate in remaining:
                if candidate is container:
                    continue

                try:
                    # Check compatibility without permanently inserting
                    container.insert_other_trailer(candidate)
                    container.contained_trailer = None
                    candidates.append(candidate)
                except Exception:
                    continue

            if not candidates:
                continue

            # Pick the longest trailer that fits
            best_candidate = max(
                candidates,
                key=lambda trailer: (
                    trailer.length or 0,
                    trailer.width or 0,
                    trailer.height or 0,
                ),
            )

            container.insert_other_trailer(best_candidate)
            remaining.remove(best_candidate)

        return remaining

    def stack_all(self, trailers: list[dt.Trailer], max_results: int = 25):
        all_results = []

        trailers = Stacker.pack_contained_trailers_greedy(trailers)

        for lorry_candidate in self.valid_lorries:
            
            Stacker._stack_recursive_all(
                stack_positions=lorry_candidate.stacks,
                position_index=0,
                available_trailers=trailers.copy(),
                final_stacks=[],
                all_results=all_results,
                max_results=max_results,
            )

            if len(all_results) >= max_results:
                break

        return all_results


    def _stack_recursive_all(
        stack_positions,
        position_index: int,
        available_trailers: list[dt.Trailer],
        final_stacks: list[dt.Stack],
        all_results: list[list[dt.Stack]],
        max_results: int,
    ):
        if len(all_results) >= max_results:
            return

        if position_index == len(stack_positions):
            if len(available_trailers) == 0:
                all_results.append(final_stacks)
            return

        if len(available_trailers) == 0:
            return

        stack_position = stack_positions[position_index]

        for stack_template in stack_position:
            fill_options = stack_template.fill_options(available_trailers)

            for filled_stack, used_indices in fill_options:
                next_available_trailers = Stacker.remove_at(
                    available_trailers,
                    used_indices,
                )

                Stacker._stack_recursive_all(
                    stack_positions=stack_positions,
                    position_index=position_index + 1,
                    available_trailers=next_available_trailers,
                    final_stacks=final_stacks + [filled_stack],
                    all_results=all_results,
                    max_results=max_results,
                )

    def stack_partial(self, trailers: list[dt.Trailer], max_results: int = 10):
        partial_results = []

        trailers = Stacker.pack_contained_trailers_greedy(trailers)

        for lorry_candidate in self.valid_lorries:
            Stacker._stack_partial_recursive(
                stack_positions=lorry_candidate.stacks,
                position_index=0,
                available_trailers=trailers.copy(),
                final_stacks=[],
                partial_results=partial_results,
            )

        partial_results.sort(
            key=lambda result: (
                result["placed_count"],
                -len(result["unplaced_trailers"]),
                result["filled_positions"],
            ),
            reverse=True,
        )

        return partial_results[:max_results]


    def _stack_partial_recursive(
        stack_positions,
        position_index: int,
        available_trailers: list[dt.Trailer],
        final_stacks: list[dt.Stack],
        partial_results: list[dict],
    ):
        placed_count = sum(len(stack.trailers) for stack in final_stacks)

        if len(final_stacks) > 1:
            partial_results.append({
                "stacks": final_stacks,
                "placed_count": placed_count,
                "unplaced_trailers": available_trailers.copy(),
                "filled_positions": len(final_stacks),
                "total_positions": len(stack_positions),
                "score": placed_count,
            })

        if position_index == len(stack_positions):
            return

        if len(available_trailers) == 0:
            return

        stack_position = stack_positions[position_index]

        for stack_template in stack_position:
            fill_options = stack_template.fill_options(available_trailers)

            for filled_stack, used_indices in fill_options:
                next_available_trailers = Stacker.remove_at(
                    available_trailers,
                    used_indices,
                )

                Stacker._stack_partial_recursive(
                    stack_positions=stack_positions,
                    position_index=position_index + 1,
                    available_trailers=next_available_trailers,
                    final_stacks=final_stacks + [filled_stack],
                    partial_results=partial_results,
                )