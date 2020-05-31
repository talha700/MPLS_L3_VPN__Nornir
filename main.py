import time
from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result


start_timer=time.perf_counter()

nr = InitNornir(config_file="config.yaml" , dry_run=False)

def mpls_conf(task):

    r = task.run(task=text.template_file,
                name="MPLS layer 3 vpn",
                template="mpls.jinja2",
                path=f"templates/{task.host.groups[0]}")

    task.host["config"] = r.result
    task.run(task=networking.netmiko_send_config,
           name="Loading configuration",
          config_commands= task.host["config"])

result=nr.run(task=mpls_conf)
print_result(result)

end_timer=time.perf_counter()
timer=f'Executed in= {round(end_timer-start_timer, 1)} second(s)'
print(timer)


