import arxiv

# Initialize the arxiv client
client = arxiv.Client()

search = arxiv.Search(
    query="quantum", max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate
)

results = client.results(search)

for r in client.results(search):
    print(r.title)
