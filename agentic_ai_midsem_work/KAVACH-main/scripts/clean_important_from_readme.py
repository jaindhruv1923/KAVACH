with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

# Any remaining important/ paths
text = text.replace("important/03_Documentation/", "03_Documentation/")
text = text.replace("important/01_KAVACH_Platform/", "01_KAVACH_Platform/")
text = text.replace("important/02_Banking_and_Results_Dashboard/", "02_Banking_and_Results_Dashboard/")
text = text.replace("important/", "")

with open("README.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Remaining important/ cleaned from README.md")
