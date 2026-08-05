import re


class DocumentStructureChunker:

    def split_text(
        self,
        text: str,
    ) -> list[str]:

        sections = re.split(
            r"\n\s*\n",
            text,
        )

        chunks = []

        current_chunk = ""

        max_chunk_size = 1000

        for section in sections:

            section = section.strip()

            if not section:
                continue

            if (
                len(current_chunk)
                + len(section)
                < max_chunk_size
            ):

                current_chunk += (
                    section + "\n\n"
                )

            else:

                if current_chunk:

                    chunks.append(
                        current_chunk.strip()
                    )

                current_chunk = (
                    section + "\n\n"
                )

        if current_chunk:

            chunks.append(
                current_chunk.strip()
            )

        return chunks