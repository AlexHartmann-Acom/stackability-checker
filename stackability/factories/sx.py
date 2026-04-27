import stackability.datatypes as datatypes

FRONT_STACKS = [
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['BSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['PSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2,3]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['MSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2,3]]
    
    )
]

MIDDLE_STACKS = [
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['BSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['PSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2,3]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['MSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2,3,4]]
    
    )
]

REAR_STACKS = [
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['PSX']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['BSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2], [3]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['MSX']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['BSX']
            ),
            
        ],
        blueprint_indices=[[0,1],[2,3]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['MSX']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['PSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2],[3,4]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['MSX']
            ),
            
        ],
        blueprint_indices=[[0,1,2,3,4]]
    
    )
]

def base_with(
    position,
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
    if position == 'FRONT':
        stacks = FRONT_STACKS
    elif position == 'MIDDLE':
        stacks = MIDDLE_STACKS
    elif position == 'REAR':
        stacks = REAR_STACKS
    else:
        raise ValueError("position must be 'FRONT', 'MIDDLE' or 'REAR'")

    def apply_min_max(bp, min_attr, max_attr, new_min, new_max) -> bool:
        current_min = getattr(bp, min_attr)
        current_max = getattr(bp, max_attr)

        # Check incompatibility first
        if new_min is not None and current_max is not None and new_min > current_max:
            return False

        if new_max is not None and current_min is not None and new_max < current_min:
            return False

        # Merge constraints
        if new_min is not None:
            if current_min is None:
                setattr(bp, min_attr, new_min)
            else:
                setattr(bp, min_attr, max(current_min, new_min))

        if new_max is not None:
            if current_max is None:
                setattr(bp, max_attr, new_max)
            else:
                setattr(bp, max_attr, min(current_max, new_max))

        return True

    def apply_allowed_models(bp, new_allowed_models) -> bool:
        if new_allowed_models is None:
            return True

        current_allowed_models = bp.allowed_models

        if current_allowed_models is None:
            bp.allowed_models = new_allowed_models.copy()
            return True

        intersection = [
            model
            for model in current_allowed_models
            if model in new_allowed_models
        ]

        if len(intersection) == 0:
            return False

        bp.allowed_models = intersection
        return True

    new_stacks = []

    for base_stack in stacks:
        stack = base_stack.copy()
        stack_is_valid = True

        for trailer_bp in stack.trailer_blueprints:
            if not apply_allowed_models(trailer_bp, allowed_models):
                stack_is_valid = False
                break

            if not apply_min_max(trailer_bp, "min_height", "max_height", min_height, max_height):
                stack_is_valid = False
                break

            if not apply_min_max(trailer_bp, "min_width", "max_width", min_width, max_width):
                stack_is_valid = False
                break

            if not apply_min_max(trailer_bp, "min_length", "max_length", min_length, max_length):
                stack_is_valid = False
                break

            if not apply_min_max(trailer_bp, "min_axles", "max_axles", min_axles, max_axles):
                stack_is_valid = False
                break

        if stack_is_valid:
            new_stacks.append(stack)

    return new_stacks

valid_lorries = [
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=325
            ),
            base_with(
                'MIDDLE',
                allowed_models=['MSX']
            ),
            base_with(
                'REAR',
                allowed_models=['MSX']
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=405
            ),
            base_with(
                'MIDDLE',
                max_length=405
            ),
            base_with(
                'REAR',
                allowed_models=['MSX']
            )
        ]
    ),
    # 4 Stacks
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=251
            ),
            base_with(
                'MIDDLE',
                max_length=305,
                max_width=178
            ),
            base_with(
                'MIDDLE',
                max_length=325,
            ),
            base_with(
                'REAR',
                allowed_models=['MSX']
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=251
            ),
            base_with(
                'MIDDLE',
                max_length=301,
                max_width=178
            ),
            base_with(
                'MIDDLE',
                max_length=301,
            ),
            base_with(
                'REAR',
                allowed_models=['MSX']
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=251
            ),
            base_with(
                'MIDDLE',
                max_length=305,
                max_width=178
            ),
            base_with(
                'MIDDLE',
                max_length=325,
            ),
            base_with(
                'REAR',
                max_length=325
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=301
            ),
            base_with(
                'MIDDLE',
                max_length=301,
                max_width=178
            ),
            base_with(
                'MIDDLE',
                max_length=301,
            ),
            base_with(
                'REAR',
                max_length=325
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=305,
                max_width=178
            ),
            base_with(
                'MIDDLE',
                max_length=305,
                max_width=178
            ),
            base_with(
                'MIDDLE',
                max_length=325,
            ),
            base_with(
                'REAR',
                max_length=325
            )
        ]
    ),
    # 5 Stacks
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=251,
            ),
            base_with(
                'MIDDLE',
                max_length=251,
            ),
            base_with(
                'MIDDLE',
                max_length=205,
            ),
            base_with(
                'MIDDLE',
                max_length=205,
            ),
            base_with(
                'REAR',
                max_length=405
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=251,
            ),
            base_with(
                'MIDDLE',
                max_length=251,
            ),
            base_with(
                'MIDDLE',
                max_length=251,
            ),
            base_with(
                'MIDDLE',
                max_length=251,
            ),
            base_with(
                'REAR',
                max_length=251
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=251,
                max_axles=1
            ),
            base_with(
                'MIDDLE',
                max_length=251,
                max_axles=1
            ),
            base_with(
                'MIDDLE',
                max_length=251,
                max_axles=1
            ),
            base_with(
                'MIDDLE',
                max_length=205,
                max_axles=1
            ),
            base_with(
                'REAR',
                max_length=325
            )
        ]
    ),
]

def remove_at(lst, indices):
    new_lst = []
    for idx, el in enumerate(lst):
        if idx not in indices:
            new_lst.append(el)

    return new_lst

def stack(trailers: list[datatypes.Trailer]):
    for lorry_candidate in valid_lorries:
        result = _stack_recursive(
            stack_positions=lorry_candidate.stacks,
            position_index=0,
            available_trailers=trailers.copy(),
            final_stacks=[],
        )

        if result is not None:
            return result

    return None


def _stack_recursive(
    stack_positions,
    position_index: int,
    available_trailers: list[datatypes.Trailer],
    final_stacks: list[datatypes.Stack],
):
    if position_index == len(stack_positions):
        if len(available_trailers) == 0:
            return final_stacks
        return None

    if len(available_trailers) == 0:
        return None

    # Simple pruning: if remaining positions cannot consume all trailers, stop early.
    min_needed = 0
    max_needed = 0

    for stack_position in stack_positions[position_index:]:
        counts = [
            max(list(map(max, stack_template.blueprint_indices))) + 1
            for stack_template in stack_position
        ]

        min_needed += min(counts)
        max_needed += max(counts)

    if len(available_trailers) < min_needed:
        return None

    if len(available_trailers) > max_needed:
        return None

    stack_position = stack_positions[position_index]

    for stack_template in stack_position:
        fill_options = stack_template.fill_options(available_trailers)

        for filled_stack, used_indices in fill_options:
            next_available_trailers = remove_at(
                available_trailers,
                used_indices,
            )

            result = _stack_recursive(
                stack_positions=stack_positions,
                position_index=position_index + 1,
                available_trailers=next_available_trailers,
                final_stacks=final_stacks + [filled_stack],
            )

            if result is not None:
                return result

    return None


def print_trailers(label: str, trailers: list[datatypes.Trailer]):
    print(label)

    if len(trailers) == 0:
        print("  <none>")
        return

    for idx, trailer in enumerate(trailers):
        print(
            f"  [{idx}] "
            f"sku={getattr(trailer, 'sku', None)}, "
            f"model={getattr(trailer, 'model_name', None)}, "
            f"L={getattr(trailer, 'length', None)}, "
            f"W={getattr(trailer, 'width', None)}, "
            f"H={getattr(trailer, 'height', None)}, "
            f"axles={getattr(trailer, 'axles', None)}"
        )


def print_stacks(label: str, stacks: list[datatypes.Stack]):
    print(label)

    if len(stacks) == 0:
        print("  <none>")
        return

    for stack_idx, stack in enumerate(stacks):
        print(f"  Stack {stack_idx + 1}:")
        print_trailers("    trailers", stack.trailers)


def print_stack_blueprints(label: str, stack: datatypes.Stack):
    print(label)

    for bp_idx, trailer_bp in enumerate(stack.trailer_blueprints):
        indices = stack.blueprint_indices[bp_idx]

        print(
            f"  BP {bp_idx}, positions={indices}, "
            f"models={getattr(trailer_bp, 'allowed_models', None)}, "
            f"L={getattr(trailer_bp, 'min_length', None)}"
            f"-{getattr(trailer_bp, 'max_length', None)}, "
            f"W={getattr(trailer_bp, 'min_width', None)}"
            f"-{getattr(trailer_bp, 'max_width', None)}, "
            f"H={getattr(trailer_bp, 'min_height', None)}"
            f"-{getattr(trailer_bp, 'max_height', None)}, "
            f"axles={getattr(trailer_bp, 'min_axles', None)}"
            f"-{getattr(trailer_bp, 'max_axles', None)}"
        )

def stack_all(trailers: list[datatypes.Trailer], max_results: int = 25):
    all_results = []

    for lorry_candidate in valid_lorries:
        _stack_recursive_all(
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
    available_trailers: list[datatypes.Trailer],
    final_stacks: list[datatypes.Stack],
    all_results: list[list[datatypes.Stack]],
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
            next_available_trailers = remove_at(
                available_trailers,
                used_indices,
            )

            _stack_recursive_all(
                stack_positions=stack_positions,
                position_index=position_index + 1,
                available_trailers=next_available_trailers,
                final_stacks=final_stacks + [filled_stack],
                all_results=all_results,
                max_results=max_results,
            )