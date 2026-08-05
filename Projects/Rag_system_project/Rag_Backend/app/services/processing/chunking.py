from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


class RecursiveChunker:

    def __init__(self):

        self.splitter = (
            RecursiveCharacterTextSplitter(

                chunk_size=1000,

                chunk_overlap=200,

                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    "",
                ],
            )
        )

    def split_text(
            self,
            text: str,
        ) -> list[str]:

        return self.splitter.split_text(text)