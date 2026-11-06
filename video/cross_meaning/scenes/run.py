import sys, importlib
mod = importlib.import_module(sys.argv[1])
stages = sys.argv[sys.argv.index('--stages') + 1] if '--stages' in sys.argv else None
mod.main(sys.argv[2], stages)
