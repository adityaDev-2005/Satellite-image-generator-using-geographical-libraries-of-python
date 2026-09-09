# The job of this file is to convert human-readable req. -> structured info.
# eg query : vegetation near Vijaywada so the words are split around the connector words (here it is the word "near")
# while(True):

def parse_query(query):
    query = query.strip().lower()
    separators = [" near ", " around ", " in "]
    for separator in separators:
        if separator in query:
            analysis, location = query.split(separator, 1)
            return {
                "analysis": analysis.strip(),
                "location": location.strip()
            }

    return None


if __name__ == "__main__":
    test_query = input("Enter your geographic query: ")
    result = parse_query(test_query)
    if result:
        print("\nParsed query:")
        print(f"Analysis : {result['analysis']}")
        print(f"Location : {result['location']}")
    else:
        print("\nCould not understand the query.")
        print("Try something like:")
        print("  vegetation near Vijayawada")
        print("  water around Kankipadu")
        print("  forest near Bengaluru")            