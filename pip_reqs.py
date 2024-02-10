def modify_lines(filename):
    """
    Reads a file, removes everything after the second equal sign for each line,
    and doubles the first equal sign.

    Args:
      filename: The path to the file to be modified.

    Returns:
      A list of modified lines.
    """
    modified_lines = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.split("=")
            if len(parts) >= 2:
                # Ensure there's at least one character after the '='
                if len(parts[1]) > 0:
                    # Join all parts before the second '=' with double '='
                    modified_line = "==".join(parts[:2]) + "\n"
                else:
                    # Handle case where there's no content after the first '='
                    modified_line = line
            else:
                # Skip lines with no '=' or only one '='
                modified_line = line
            modified_lines.append(modified_line)
    return modified_lines


# Example usage
modified_lines = modify_lines("conda_requirements.txt")
with open("requirements.txt", "w") as f:
    f.write("".join(modified_lines))
