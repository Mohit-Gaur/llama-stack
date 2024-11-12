# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from enum import Enum
from typing import (
    Annotated,
    List,
    Literal,
    Optional,
    Protocol,
    runtime_checkable,
    Union,
)

from llama_models.schema_utils import json_schema_type, webmethod

from pydantic import BaseModel, Field

from llama_stack.apis.resource import Resource, ResourceType


@json_schema_type
class MemoryBankType(Enum):
    vector = "vector"
    keyvalue = "keyvalue"
    keyword = "keyword"
    graph = "graph"


@json_schema_type
class VectorMemoryBank(Resource):
    type: Literal[ResourceType.memory_bank.value] = ResourceType.memory_bank.value
    memory_bank_type: Literal[MemoryBankType.vector.value] = MemoryBankType.vector.value
    embedding_model: str
    chunk_size_in_tokens: int
    overlap_size_in_tokens: Optional[int] = None


@json_schema_type
class KeyValueMemoryBank(Resource):
    type: Literal[ResourceType.memory_bank.value] = ResourceType.memory_bank.value
    memory_bank_type: Literal[MemoryBankType.keyvalue.value] = (
        MemoryBankType.keyvalue.value
    )


@json_schema_type
class KeywordMemoryBank(Resource):
    type: Literal[ResourceType.memory_bank.value] = ResourceType.memory_bank.value
    memory_bank_type: Literal[MemoryBankType.keyword.value] = (
        MemoryBankType.keyword.value
    )


@json_schema_type
class GraphMemoryBank(Resource):
    type: Literal[ResourceType.memory_bank.value] = ResourceType.memory_bank.value
    memory_bank_type: Literal[MemoryBankType.graph.value] = MemoryBankType.graph.value


@json_schema_type
class VectorMemoryBankParams(BaseModel):
    memory_bank_type: Literal[MemoryBankType.vector.value] = MemoryBankType.vector.value
    embedding_model: str
    chunk_size_in_tokens: int
    overlap_size_in_tokens: Optional[int] = None


@json_schema_type
class KeyValueMemoryBankParams(BaseModel):
    memory_bank_type: Literal[MemoryBankType.keyvalue.value] = (
        MemoryBankType.keyvalue.value
    )


@json_schema_type
class KeywordMemoryBankParams(BaseModel):
    memory_bank_type: Literal[MemoryBankType.keyword.value] = (
        MemoryBankType.keyword.value
    )


@json_schema_type
class GraphMemoryBankParams(BaseModel):
    memory_bank_type: Literal[MemoryBankType.graph.value] = MemoryBankType.graph.value


MemoryBank = Annotated[
    Union[
        VectorMemoryBank,
        KeyValueMemoryBank,
        KeywordMemoryBank,
        GraphMemoryBank,
    ],
    Field(discriminator="memory_bank_type"),
]

BankParams = Annotated[
    Union[
        VectorMemoryBankParams,
        KeyValueMemoryBankParams,
        KeywordMemoryBankParams,
        GraphMemoryBankParams,
    ],
    Field(discriminator="memory_bank_type"),
]


@runtime_checkable
class MemoryBanks(Protocol):
    @webmethod(route="/memory_banks/list", method="GET")
    async def list_memory_banks(self) -> List[MemoryBank]: ...

    @webmethod(route="/memory_banks/get", method="GET")
    async def get_memory_bank(self, memory_bank_id: str) -> Optional[MemoryBank]: ...

    @webmethod(route="/memory_banks/register", method="POST")
    async def register_memory_bank(
        self,
        memory_bank_id: str,
        params: BankParams,
        provider_id: Optional[str] = None,
        provider_memorybank_id: Optional[str] = None,
    ) -> MemoryBank: ...
