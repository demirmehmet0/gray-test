from typing import Optional, Union, Literal, List, Dict
from pydantic import Field, validator, BaseModel

from sdks.novavision.src.base.model import (
    Package,
    Input,
    Output,
    Image,
    Config,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,

    BoundingBox, KeyPoints, Detection
)



class InputTimeStamp(Input):
    name: Literal["inputTimeStamp"] = "inputTimeStamp"
    value: Union[List[Image], Image, List[Detection], Detection, Dict, List]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, Detection):
            return "object"
        elif isinstance(value, dict):
            return "dict"
        elif isinstance(value, list):
            return "list"
    class Config:
        title = "Data"

class TimeStampFormat(Config):
    """
        Please enter the date and time in any format you prefer.
    """
    name: Literal["TimeStampFormat"] = "TimeStampFormat"
    value: str = Field(default="%Y-%m-%d %H:%M:%S:%f")
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Time Stamp Format"


class OutputTimeStamp(Output):
    name: Literal["outputTimeStamp"] = "outputTimeStamp"
    value: Union[Dict]
    type: str = "dict"

    class Config:
        title = "Time Stamp Format"

class NowConfigs(Configs):
    timeStampFormat: TimeStampFormat

class NowOutputs(Outputs):
    outputTimeStamp: OutputTimeStamp

    class Config:
        title = "Time Stamp Outputs"

class NowRequest(Request):
    configs: NowConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class NowResponse(Response):
    outputs: NowOutputs

class NowExecutor(Config):
    name: Literal["Now"] = "Now"
    value: Union[NowRequest, NowResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = " Now Executor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConvertTimeInput(Inputs):
    inputTimeStamp: InputTimeStamp

class ConvertTimeConfigs(Configs):
    timeStampFormat: TimeStampFormat

class ConvertTimeOutputs(Outputs):
    outputTimeStamp: OutputTimeStamp

    class Config:
        title = "Time Stamp Outputs"

class ConvertTimeRequest(Request):
    inputs: Optional[ConvertTimeInput]
    configs: ConvertTimeConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class ConvertTimeResponse(Response):
    outputs: ConvertTimeOutputs

class ConvertTimeExecutor(Config):
    name: Literal["ConvertTime"] = "ConvertTime"
    value: Union[ConvertTimeRequest, ConvertTimeResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = " Convert Time"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[NowExecutor, ConvertTimeExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["TimeStamp"] = "TimeStamp"

    class Config:
        title = "Package Model"
