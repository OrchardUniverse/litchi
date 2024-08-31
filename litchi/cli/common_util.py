import logging

class CommandCommonUtil:
    @staticmethod    
    def extract_query(query_or_file: str):
        if query_or_file.lower().endswith(".txt"):
            with open(query_or_file, "r") as f:
                query = f.read()
                logging.info(f"Read the requiremtn file in {query_or_file} to get actual querty:\n{query}")
        else:
            query = query_or_file

        return query