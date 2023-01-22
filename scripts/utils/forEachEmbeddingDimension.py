import traceback
from typing import Callable
from utils.arguments import KaleSettings
from utils.exceptions import KaleException, AmarException, ElliotException

def forEachEmbeddingDimension(kaleSettings: KaleSettings, f: Callable[[KaleSettings, int], None]):
    statuses = {}

    def updateStatusWithError(e: BaseException, dim: int, msg: str):
        traceback.print_exc()
        statuses[dim] = (f"something went wrong while {msg}", e)

    for dim in kaleSettings.dims:
        print(f"\nSTARTING ON DIMENSION {dim}:\n")

        try:
            f(kaleSettings, dim)
            statuses[dim] = ("each requested process was successfully completed", "no problems occurred")
            
            print(f"\nSUCCESSFULLY COMPLETED ALL OPERATIONS ON DIMENSION {dim}.")
        except KaleException as e:
            updateStatusWithError(e, dim, "learning the embeddings with KALE")
        except AmarException as e:
            updateStatusWithError(e, dim, "training the model with AMAR")
        except ElliotException as e:
            updateStatusWithError(e, dim, f"running an Elliot experiment")
        except KeyboardInterrupt as e:
            print("\nPROCESS WAS HALTED BY THE USER.\n")
            break
        except BaseException as e:
            updateStatusWithError(e, dim, "executing an unknown phase of the process")
    
    print("\nRESULTS:")

    for dim, (msg, e) in statuses.items():
        print(f"Dimension {dim} > {msg} ({e}).")