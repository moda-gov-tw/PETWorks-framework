import os.path as path
import yaml


class Config:
    def __init__(self, configPath) -> None:
        self.rawConfigPath = configPath
        self.rawConfigFolderPath = path.dirname(configPath)

        if path.exists(self.rawConfigPath):
            with open(self.rawConfigPath, "r") as stream:
                self.rawConfig = yaml.load(stream, Loader=yaml.CLoader)

        else:
            self.rawConfig = {}

    @property
    def attributeTypes(self):
        if (
            "DATASET" not in self.rawConfig
            or "ATTRIBUTE_TYPE" not in self.rawConfig["DATASET"]
        ):
            return {}

        typeMapping = {
            column: attributeType.lower()
            for attributeType, columns in self.rawConfig["DATASET"][
                "ATTRIBUTE_TYPE"
            ].items()
            for column in columns
        }

        return typeMapping

    @property
    def hierarchy(self):
        if (
            "DATASET" not in self.rawConfig
            or "HIERARCHY" not in self.rawConfig["DATASET"]
        ):
            return None

        if self.rawConfigFolderPath is not None:
            pathToHierarchy = path.join(
                self.rawConfigFolderPath,
                self.rawConfig["DATASET"]["HIERARCHY"],
            )
        else:
            pathToHierarchy = self.rawConfig["DATASET"]["HIERARCHY"]

        return pathToHierarchy

    @staticmethod
    def getDefaultConfigPath(pathToData):
        dataName = path.splitext(path.basename(pathToData))[0]
        rawConfigFolderPath = path.dirname(pathToData)

        rawConfigPath = path.join(rawConfigFolderPath, f"{dataName}.yaml")

        return rawConfigPath
