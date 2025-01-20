import sys
from openai import OpenAI
import openai
import cfg
import unpwdkeys


def main():
    if cfg.proxy:
        openai.proxy = cfg.proxy
    llms = { role:{'client': OpenAI(api_key=llm['apikey'], base_url=llm['base_url']), 'model':llm['model']} for role, llm in cfg.llms.items() }
    for task in cfg.tasks:
        print('\nTask:\n' + task)
        messages = { roleid:[{'role':'user', 'content':[{'type':'text', 'text':role['role'] + '\nTask:\n' + task}]}] for roleid, role in cfg.roles.items() }
        for i in range(cfg.max_iterations):
            response = cfg.stop_word
            for roleid, role in cfg.roles.items():
                response = llms[roleid]['client'].chat.completions.create(model=llms[roleid]['model'], messages=messages[roleid], stream=False)
                response = response.choices[0].message.content
                print('\nIteration {0}, Role {1}, Response:\n'.format(str(i), role['title']))
                print(response)
                for rid, message in messages.items():
                    if roleid == rid:
                        message.append({'role':'assistant', 'content':[{'type':'text', 'text':response}]})
                    else:
                        message.append({'role':'user', 'content':[{'type':'text', 'text':response}]})
            if i>=cfg.min_iterations and cfg.stop_word in response:
                break
    return 0

if __name__ == "__main__":
    sys.exit(main())
