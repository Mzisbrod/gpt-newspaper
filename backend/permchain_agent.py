# This file contains the agent executor for the permchain agent.
from permchain import Channel, Pregel
from permchain.channels import LastValue
from permchain.checkpoint.base import BaseCheckpointAdapter


def get_agent_executor(
    search,
    curator,
    writer,
    checkpoint: BaseCheckpointAdapter,
) -> Pregel:

    search_chain = Channel.subscribe_to(["question"]) | search | Channel.write_to("sources")
    curator_chain = Channel.subscribe_to(["sources"]).join(['question']) | curator | Channel.write_to("context")
    writer_chain = Channel.subscribe_to(["context"]).join(['question']) | writer | Channel.write_to("draft")
    designer_chain = Channel.subscribe_to(["draft"]).join(['question']) | writer | Channel.write_to("final_report")

    return Pregel(
        chains={"search": search_chain, "curator": curator_chain, "writer": writer_chain, "designer": designer_chain},
        channels={
            "question": LastValue(str),
            "sources": LastValue(str),
            "context": LastValue(str),
            "draft": LastValue(str),
            "final_report": LastValue(str),
        },
        input=["question"],
        output=["final_report"],
        checkpoint=checkpoint,
    )