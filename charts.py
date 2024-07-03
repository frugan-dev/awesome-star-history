import yaml
import urllib.parse

def generate_chart_markdown(category, subcategory, repos, is_first=False):
    repo_list = ",".join(repos)
    encoded_repos = urllib.parse.quote(repo_list)
    chart_url = f"https://api.star-history.com/svg?repos={encoded_repos}&type=Date"
    star_history_url = f"https://star-history.com/#{repo_list}&Date"
    
    chart_md = f"""
[![Star History Chart]({chart_url})]({star_history_url})
"""
    
    details = f"""
<details>
<summary>{subcategory}</summary>
{chart_md}
</details>
"""

    if is_first:
        return f"""
### {category}
{details}"""
    else:
        return details

def main():
    with open('repo.yml', 'r') as file:
        categories = yaml.safe_load(file)

    charts_markdown = ""
    for category, subcategories in categories.items():
        is_first = True
        for subcategory, repos in subcategories.items():
            if is_first:
                charts_markdown += generate_chart_markdown(category, subcategory, repos, is_first)
                is_first = False
            else:
                charts_markdown += generate_chart_markdown(category, subcategory, repos)

    with open('README.md', 'r') as file:
        readme_content = file.read()

    start_marker = "<!-- START_CHARTS -->"
    end_marker = "<!-- END_CHARTS -->"
    new_content = f"{start_marker}\n{charts_markdown}\n{end_marker}"
    
    updated_readme = readme_content.split(start_marker)[0] + new_content + readme_content.split(end_marker)[1]

    with open('README.md', 'w') as file:
        file.write(updated_readme)

if __name__ == "__main__":
    main()