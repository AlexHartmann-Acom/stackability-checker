SPECIAL_MODEL_CATEGORIES = [
    'O',
    'R',
    'HT',
    'VT1',
    'VT2',
    'VT3',
    'VT4'
]

class Trailer:
    height: int
    width: int
    length: int
    axles: int
    sku: str
    model_name : str
    contained_trailer = None

    def __init__(self, sku, height, width, length, axles, model_name):
        self.sku = sku
        self.height = height
        self.width = width
        self.length = length
        self.axles = axles
        self.model_name = model_name

    def factory_name(self) -> str:
        FACTORY_STRINGS = [
            'SX',
            'GT'
        ]
        for factory_string in FACTORY_STRINGS:
            if factory_string in self.model_name:
                return factory_string
        return factory_string
    
    def model_category(self):
        return self.model_name.split(' ')[0]
    
    def insert_other_trailer(self, trailer : 'Trailer'):
        if trailer.length > self.length or trailer.width > self.width or trailer.height > self.height:
            raise Exception(f'Cannot store a trailer in another that is smaller')
        
        if 'VT3' not in self.model_category() and 'VT4' not in self.model_category():
            raise Exception(f'This trailer type ({self.model_category()}) cannot contain another trailer')
        
        if self.contained_trailer is not None:
            raise Exception(f'This trailer already contains another trailer')
        
        if 'VT3' in self.model_category():
            #Can insert HT
            if 'HT' not in trailer.model_category():
                raise Exception(f'{trailer.model_category()} cannot be inserted into {self.model_category()}')
            else:
                self.contained_trailer = trailer
                return

        if 'VT4' in self.model_category():
            #Can insert VT1
            if 'VT1' not in trailer.model_category():
                raise Exception(f'{trailer.model_category()} cannot be inserted into {self.model_category()}')
            else:
                self.contained_trailer = trailer
                return
    

class TrailerBlueprint:
    min_height: int
    max_height: int
    min_width: int
    max_width: int
    min_length: int
    max_length: int
    allowed_models: list[str]
    min_axles: int
    max_axles: int

    def __init__(
        self,
        allowed_models=None,
        min_height=None,
        max_height=None,
        min_width=None,
        max_width=None,
        min_length=None,
        max_length=None,
        min_axles=None,
        max_axles=None
    ):
        self.min_height = min_height
        self.max_height = max_height
        self.min_width = min_width
        self.max_width = max_width
        self.min_length = min_length
        self.max_length = max_length
        self.allowed_models = allowed_models
        self.min_axles = min_axles
        self.max_axles = max_axles

    def copy(self):
        return TrailerBlueprint(
            allowed_models=self.allowed_models.copy() if self.allowed_models is not None else None
            if self.allowed_models is not None
            else None,
            min_height=self.min_height,
            max_height=self.max_height,
            min_width=self.min_width,
            max_width=self.max_width,
            min_length=self.min_length,
            max_length=self.max_length,
            min_axles=self.min_axles,
            max_axles=self.max_axles,
        )

    # if None, no check
    def check(self, trailer: Trailer):
        if self.min_height is not None:
            if trailer.height is None or trailer.height < self.min_height:
                return False

        if self.max_height is not None:
            if trailer.height is None or trailer.height > self.max_height:
                return False

        if self.min_width is not None:
            if trailer.width is None or trailer.width < self.min_width:
                return False

        if self.max_width is not None:
            if trailer.width is None or trailer.width > self.max_width:
                return False

        if self.min_length is not None:
            if trailer.length is None or trailer.length < self.min_length:
                return False

        if self.max_length is not None:
            if trailer.length is None or trailer.length > self.max_length:
                return False

        if self.min_axles is not None:
            if trailer.axles is None or trailer.axles < self.min_axles:
                return False

        if self.max_axles is not None:
            if trailer.axles is None or trailer.axles > self.max_axles:
                return False

        if self.allowed_models is not None:
            if trailer.model_category() is None or trailer.model_category() not in self.allowed_models:
                return False

        return True


class Stack:
    trailers: list[Trailer]
    trailer_blueprints: list[TrailerBlueprint]
    blueprint_indices: list[list[int]]
    max_total_height: int
    max_width: int

    def __repr__(self):
        return f'Stack ({len(self.trailers)}) = [{list(map(lambda x: f"{x.model_category()} <{x.length}>", self.trailers))}]'

    def __init__(self, trailer_blueprints, blueprint_indices, trailers=None, max_total_height=None, max_width=None):
        self.trailer_blueprints = trailer_blueprints
        self.blueprint_indices = blueprint_indices
        self.max_total_height = max_total_height
        self.max_width = max_width

        if trailers is None:
            self.trailers = []
        else:
            self.trailers = trailers

    def copy(self):
        return Stack(
            trailer_blueprints=[
                trailer_blueprint.copy()
                for trailer_blueprint in self.trailer_blueprints
            ],
            blueprint_indices=[
                blueprint_index.copy()
                for blueprint_index in self.blueprint_indices
            ],
            trailers=self.trailers.copy()
        )

    def fill(self, trailers_in: list[Trailer]) -> tuple[bool, list[int]]:
        if len(self.trailers) != 0:
            raise Exception('Trying to fill stack that already has trailers')

        target_trailer_count = max(list(map(max, self.blueprint_indices))) + 1

        print(f'Trying to fill stack. Target count: {target_trailer_count}')
        print(f'Available trailers: {trailers_in}')

        # Build one blueprint requirement per physical trailer position in the stack
        position_blueprints: list[TrailerBlueprint | None] = [None] * target_trailer_count

        for bp_idx, trailer_bp in enumerate(self.trailer_blueprints):
            for position_idx in self.blueprint_indices[bp_idx]:
                position_blueprints[position_idx] = trailer_bp

        if any(bp is None for bp in position_blueprints):
            raise Exception(
                f'Invalid stack definition: not all positions have a blueprint. '
                f'{position_blueprints = }'
            )

        def recurse(
            position_idx: int,
            chosen_trailers: list[Trailer],
            chosen_indices: list[int],
        ) -> tuple[bool, list[Trailer], list[int]]:
            if position_idx == target_trailer_count:
                return True, chosen_trailers, chosen_indices

            trailer_bp = position_blueprints[position_idx]

            print(
                f'Looking for trailer for stack position {position_idx}. '
                f'Allowed models: {trailer_bp.allowed_models}'
            )

            for trailer_idx, trailer in enumerate(trailers_in):
                if trailer_idx in chosen_indices:
                    continue

                print(
                    f'  Checking trailer idx={trailer_idx}: '
                    f'{trailer.model_category()} <{trailer.length}>'
                )

                if not trailer_bp.check(trailer):
                    print('    -> no match')
                    continue

                print('    -> match, trying deeper')

                success, result_trailers, result_indices = recurse(
                    position_idx=position_idx + 1,
                    chosen_trailers=chosen_trailers + [trailer],
                    chosen_indices=chosen_indices + [trailer_idx],
                )

                if success:
                    return True, result_trailers, result_indices

                print(
                    f'    -> backtracking from trailer idx={trailer_idx}: '
                    f'{trailer.model_category()} <{trailer.length}>'
                )

            print(f'No valid trailer found for stack position {position_idx}')
            return False, [], []

        success, chosen_trailers, chosen_indices = recurse(
            position_idx=0,
            chosen_trailers=[],
            chosen_indices=[],
        )

        if not success:
            self.trailers = []
            return False, []

        self.trailers = chosen_trailers
        return True, chosen_indices
    
    def fill_options(self, trailers_in: list[Trailer]) -> list[tuple["Stack", list[int]]]:
        if len(self.trailers) != 0:
            raise Exception("Trying to fill stack that already has trailers")

        target_trailer_count = max(list(map(max, self.blueprint_indices))) + 1

        position_blueprints: list[TrailerBlueprint | None] = [None] * target_trailer_count

        for bp_idx, trailer_bp in enumerate(self.trailer_blueprints):
            for position_idx in self.blueprint_indices[bp_idx]:
                position_blueprints[position_idx] = trailer_bp

        if any(bp is None for bp in position_blueprints):
            raise Exception(
                f"Invalid stack definition: not all positions have a blueprint. "
                f"{position_blueprints = }"
            )

        results: list[tuple[Stack, list[int]]] = []
        seen_result_keys: set[tuple[int, ...]] = set()

        def trailer_key(trailer: Trailer):
            return (
                trailer.model_category(),
                trailer.length,
                trailer.width,
                trailer.height,
                trailer.axles,
            )

        def recurse(
            position_idx: int,
            chosen_trailers: list[Trailer],
            chosen_indices: list[int],
        ):
            if position_idx == target_trailer_count:
                result_key = tuple(sorted(chosen_indices))

                if result_key in seen_result_keys:
                    return

                seen_result_keys.add(result_key)

                filled_stack = self.copy()
                filled_stack.trailers = chosen_trailers.copy()
                results.append((filled_stack, chosen_indices.copy()))
                return

            trailer_bp = position_blueprints[position_idx]

            seen_trailer_keys_at_this_position = set()

            for trailer_idx, trailer in enumerate(trailers_in):
                if trailer_idx in chosen_indices:
                    continue

                key = trailer_key(trailer)

                if key in seen_trailer_keys_at_this_position:
                    continue

                if not trailer_bp.check(trailer):
                    continue

                seen_trailer_keys_at_this_position.add(key)

                recurse(
                    position_idx=position_idx + 1,
                    chosen_trailers=chosen_trailers + [trailer],
                    chosen_indices=chosen_indices + [trailer_idx],
                )

        recurse(
            position_idx=0,
            chosen_trailers=[],
            chosen_indices=[],
        )

        if self.max_total_height is not None:
            results = [
                (filled_stack, used_indices)
                for filled_stack, used_indices in results
                if sum(trailer.height for trailer in filled_stack.trailers) <= self.max_total_height
            ]

        results = [
            (filled_stack, used_indices)
            for filled_stack, used_indices in results
            if all(
                filled_stack.trailers[i].length >= filled_stack.trailers[i + 1].length
                for i in range(len(filled_stack.trailers) - 1)
            )
        ]

        return results



class Lorry:
    stacks: list[list[Stack]]

    def __init__(self, stacks):
        self.stacks = stacks