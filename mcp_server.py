from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

# TODO: Write a resource to return all doc id's
@mcp.tool(
    name="list_documents",
    description="Get a list of all available document IDs"
)
@mcp.resource("docs://documents")
def list_documents():
    """Return a list of all available document IDs"""
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.tool(
    name="get_document_content",
    description="Get the contents of a specific document by its ID"
)
@mcp.resource("docs://documents/{doc_id}")
def get_document_content(
    doc_id: str = Field(description="ID of the document to retrieve")
):
    """Return the contents of a specific document"""
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found")
    return docs[doc_id]

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.tool(
    name="rewrite_doc_markdown",
    description="Rewrite a document in proper markdown format"
)
@mcp.prompt("rewrite_markdown")
def rewrite_doc_markdown(
    doc_id: str = Field(description="ID of the document to rewrite in markdown")
):
    """Rewrite a document in markdown format"""
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found")

    content = docs[doc_id]
    return f"Please rewrite the following document in proper markdown format:\n\n{content}"

# TODO: Write a prompt to summarize a doc
@mcp.tool(
    name="summarize_doc",
    description="Generate a summary of a document"
)
@mcp.prompt("summarize")
def summarize_doc(
    doc_id: str = Field(description="ID of the document to summarize")
):
    """Generate a summary of a document"""
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found")

    content = docs[doc_id]
    return f"Please provide a concise summary of the following document:\n\n{content}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
