from runAmar import runAmar
from utils.arguments import Arguments, AmieSettings, KaleSettings, RulesFilter, AmarSettings
from runElliot import runElliot
from utils.forEachEmbeddingDimension import forEachEmbeddingDimension

def runAmarElliot(datasetFolderName: str, rulesFilter: RulesFilter, kaleSettings: KaleSettings, amarSettings: AmarSettings, dimension: int, amieSettings: AmieSettings):    
    runAmar(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings)
    runElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dimension, amieSettings)

if __name__ == "__main__":
    parser = Arguments()

    parser.addAmieSettingsOptionalArguments()
    parser.addRulesFilterArguments()
    parser.addKaleSettingsArguments()
    parser.addAmarSettingsArguments()

    (datasetFolderName, args) = parser.parse()

    amieSettings = AmieSettings(args)
    kaleSettings = KaleSettings(args)
    rulesFilter = RulesFilter(args)
    amarSettings = AmarSettings(args)

    forEachEmbeddingDimension(kaleSettings, lambda kaleSettings, dim: runAmarElliot(datasetFolderName, rulesFilter, kaleSettings, amarSettings, dim, amieSettings))