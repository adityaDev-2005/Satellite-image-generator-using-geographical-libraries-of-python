# The job of this file is to convert human-readable requirements
# into structured information.
#
# Example:
# "vegetation near Vijayawada"
# -> analysis: vegetation
# -> location: Vijayawada


ANALYSIS_ALIASES = {
    "vegetation": [
        "vegetation",
        "vegetation area",
        "vegetated area",
        "green area",
        "green areas",
        "forest",
        "forest area",
        "trees",
        "tree cover",
        "vegetation cover",
    ],
    "ndvi": [
        "ndvi",
        "vegetation index",
    ],
}

SEPARATORS = [
    " near ",
    " around ",
    " in ",
    " of ",
]


def parse_query(query):
    # Normalize whitespace and convert to lowercase
    query = " ".join(query.strip().lower().split())

    for separator in SEPARATORS:
        if separator in query:
            analysis_text, location = query.split(separator, 1)

            analysis_text = analysis_text.strip()
            location = location.strip()

            # Location must not be empty
            if not location:
                return None

            # Check whether the analysis is supported
            for analysis, aliases in ANALYSIS_ALIASES.items():
                if analysis_text in aliases:
                    return {
                        "analysis": analysis,
                        "location": location
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
        print("  vegetation area near Guntur")
        print("  green areas in Vijayawada")
        print("  forest around Bengaluru")
        print("  trees near Chennai")