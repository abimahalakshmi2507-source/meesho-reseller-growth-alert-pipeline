def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    return not any(name in text for name in reseller_names)

if __name__ == "__main__":
    reseller_names = ["Mumbai Reseller 1", "Jaipur Reseller 5"]

    safe_text = "Top reseller: ALIAS-19 from Mumbai region."
    unsafe_text = "Top reseller: Mumbai Reseller 1 from Mumbai region."

    print(alias_for("RS019"))
    print(assert_no_raw_names_leak(safe_text, reseller_names))
    print(assert_no_raw_names_leak(unsafe_text, reseller_names))
    