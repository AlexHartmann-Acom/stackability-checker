import stackability.datatypes as datatypes

FRONT_STACKS = [
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
        ],
        blueprint_indices=[[0,1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['O', 'R']
            ),
            
        ],
        blueprint_indices=[[0,1,2,3]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['HT', 'O', 'R']
            ),
            
        ],
        blueprint_indices=[[0,1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT1']
            ),
            
        ],
        blueprint_indices=[[0,1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT3']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['O', 'R'],
            ),
            
        ],
        blueprint_indices=[[0],[1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT4']
            ),
            
        ],
        blueprint_indices=[[0]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT1']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
            
        ],
        blueprint_indices=[[0], [1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT2']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['O']
            ),
            
        ],
        blueprint_indices=[[0], [1]]
    
    )
]

MIDDLE_STACKS = [
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
        ],
        blueprint_indices=[[0,1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['O', 'R']
            ),
            
        ],
        blueprint_indices=[[0,1,2,3]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['HT', 'O', 'R']
            ),
            
        ],
        blueprint_indices=[[0,1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT1']
            ),
            
        ],
        blueprint_indices=[[0,1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT3']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['O', 'R'],
            ),
            
        ],
        blueprint_indices=[[0],[1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT4']
            ),
            
        ],
        blueprint_indices=[[0]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT2']
            ),
            
            datatypes.TrailerBlueprint(
                allowed_models=['VT1']
            ),
        ],
        blueprint_indices=[[0], [1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['Ultra Low']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['O']
            ),
            
        ],
        blueprint_indices=[[0],[1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT1']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
            
        ],
        blueprint_indices=[[0], [1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT2']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['O']
            ),
            
        ],
        blueprint_indices=[[0], [1]]
    
    )
]

REAR_STACKS = [
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT2']
            ),
        ],
        blueprint_indices=[[0,1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT1']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
        ],
        blueprint_indices=[[0],[1,2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT4']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['O']
            ),
        ],
        blueprint_indices=[[0],[1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT2']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['R']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
            
        ],
        blueprint_indices=[[0],[1],[2]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['O', 'R']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
            
        ],
        blueprint_indices=[[0,1],[2,3]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT3']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['HT']
            ),
            
        ],
        blueprint_indices=[[0],[1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['VT3']
            ),
            datatypes.TrailerBlueprint(
                allowed_models=['VT1']
            ),
            
        ],
        blueprint_indices=[[0],[1]]
    
    ),
    datatypes.Stack(
        trailer_blueprints=[
            datatypes.TrailerBlueprint(
                allowed_models=['O']
            )
        ],
        blueprint_indices=[[0,1,2,3]]
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
                #allowed_models=['VT1','VT2','VT3','VT4'],
                max_length=301
            ),
            base_with(
                'MIDDLE',
                #allowed_models=['VT1','VT2','VT3','VT4'],
                max_length=301
            ),
            base_with(
                'MIDDLE',
                #allowed_models=['VT1','VT2','VT3','VT4'],
                max_length=301
            ),
            base_with(
                'REAR',
                #allowed_models=['VT1','VT2','VT3','VT4'],
                max_length=251
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=211
            ),
            base_with(
                'MIDDLE',
                max_length=251
            ),
            base_with(
                'MIDDLE',
                max_length=251
            ),
            base_with(
                'MIDDLE',
                max_length=251
            ),
            base_with(
                'REAR',
                max_length=301
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
                max_length=251
            ),
            base_with(
                'MIDDLE',
                max_length=251
            ),
            base_with(
                'MIDDLE',
                max_length=251
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
                max_length=211
            ),
            base_with(
                'MIDDLE',
                max_length=211
            ),
            base_with(
                'MIDDLE',
                max_length=211
            ),
            base_with(
                'MIDDLE',
                max_length=211
            ),
            base_with(
                'MIDDLE',
                max_length=211
            ),
            base_with(
                'REAR',
                max_length=201
            )
        ]
    ),
    datatypes.Lorry(
        stacks=[
            base_with(
                'FRONT',
                max_length=201
            ),
            base_with(
                'MIDDLE',
                max_length=201
            ),
            base_with(
                'MIDDLE',
                max_length=201
            ),
            base_with(
                'MIDDLE',
                max_length=201
            ),
            base_with(
                'MIDDLE',
                max_length=201
            ),
            base_with(
                'MIDDLE',
                max_length=201
            ),
            base_with(
                'REAR',
                max_length=201
            )
        ]
    ),
]

