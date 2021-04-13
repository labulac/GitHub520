import sys, os, time
import requests
import platform
import logging

if os.path.exists('D:\\update_git_hosts.log') == True:
    os.remove('D:\\update_git_hosts.log')
    print('delete log')

logging.basicConfig(
    level=logging.INFO,
    filename='D:\\update_git_hosts.log',
    format='%(asctime)s - %(levelname)s - %(lineno)d - %(message)s ')
logger = logging.getLogger()

logger.info("程序开始执行...")
aa=os.popen("ipconfig /flushdns").read()
print(aa)
logger.info(aa)

running_platform = platform.system()

if len(sys.argv) > 1:
    hosts_path = sys.argv[1]
elif running_platform == 'Windows':
    hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"
else:
    hosts_path = "/etc/hosts"

if not (os.access(hosts_path, os.W_OK) and os.access(hosts_path, os.R_OK)):
    logger.info(f'File {hosts_path} access denied.')
    sys.exit(1)

gh_hosts_url = "https://cdn.jsdelivr.net/gh/521xueweihan/GitHub520@main/hosts"
gh_hosts_url2 = "https://www.google.com"
gh_hosts_url3 = "https://ghproxy.com/https://raw.githubusercontent.com/labulac/GitHub520/main/hosts"
start_line = "# GitHub520 Host Start\n"
end_line = "# GitHub520 Host End\n"

while True:
    try:
        new_gh_hosts_content = ["\n"] + requests.get(
            gh_hosts_url3, timeout=10).text.splitlines(True) + ["\n"]

        hosts_file = open(hosts_path, "r+", encoding='utf-8')

        hosts_content = hosts_file.readlines() if hosts_file.readable() else []

        bk = hosts_content

        if new_gh_hosts_content.index(start_line) == True:

            try:  # if github hosts exists
                idx_start = hosts_content.index(start_line)
                idx_end = hosts_content.index(end_line)
                hosts_content = hosts_content[:
                                              idx_start] + new_gh_hosts_content + hosts_content[
                                                  idx_end + 1:]
            except:  # elif github hosts not exists
                hosts_content = hosts_content + new_gh_hosts_content

            for i in range(len(hosts_content) - 1):
                if hosts_content[i] == "\n" and hosts_content[i + 1] == "\n":
                    hosts_content[i] = ""

            hosts_file.seek(0)
            hosts_file.writelines(hosts_content)
            hosts_file.close()

            logger.info(f'{hosts_path} is updated.')

            if running_platform == 'Windows':
                aa=os.popen("ipconfig /flushdns").read()
                print(aa)
                logger.info(aa)
    except:
        logger.info("NETWORK ERROR")

    for i in range(180, 0, -1):
        print(i)
        time.sleep(1)
