"""Small clean Python example."""

contacts = {
    "Alice": "12345678",
    "Bob": "87654321",
}


def get_contact(name: str) -> str:
    return contacts.get(name, "Not found")


if __name__ == "__main__":
    print(get_contact("Bob"))