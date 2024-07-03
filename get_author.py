from markov_model import load_markov_chain, generate_random_author

class AuthorGenerator:
    def __init__(self, model_file: str, markov_length: int):
        """
        Initialize the AuthorGenerator with a pre-trained Markov model.

        Args:
            model_file (str): Path to the file containing the serialized Markov model.
            markov_length (int): Length of the Markov chain to use for generating authors.
        """
        self.model = load_markov_chain(model_file, markov_length)

    def get_author(self) -> str:
        """
        Generate a random author name using the pre-trained Markov model.

        Returns:
            str: A randomly generated author name.
        """
        return generate_random_author(self.model)

# Example usage
if __name__ == "__main__":
    # Initialize the AuthorGenerator with the model file path and markov length
    generator = AuthorGenerator('authors_markov_chain.msgpack', 2)
    # Generate and print a random author name
    print(f"Generated Author Name: {generator.get_author()}")
