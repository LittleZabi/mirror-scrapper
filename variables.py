import os
urls_list = []
root_path = os.getcwd()
# base_urls = []
file_formates = ('.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz', '.z', '.img', '.zip', '.bin', '.dmg', '.iso', '.sh', '.bat', '.toast', '.vcd', '.tar', '.cgi', '.bat', '.exe', '.jar', '.msi')
invalid_paths = ('http', '.html', 'readme' ,'README', '.txt', '.ini', '..')
downloadable_contents_urls = []
total_founds = 0
rewriteFile = True
root_url = ''
url_defaults = """#testing url
https://mirrors.lolinet.com/
#add more urls here
"""