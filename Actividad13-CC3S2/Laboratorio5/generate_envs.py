import os, json
from shutil import copyfile

# Parámetros de ejemplo para N entornos
ENVS = [
    {"name": f"app{i}", "network": f"net{i}"} for i in range(1, 11)
]

ENVS.append({
    "name": "env3", 
    "network": "net2-peered",
    "depends_on": ["app2"] 
})

MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def render_and_write(env):
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

    # 1) Copia la definición de variables (network.tf.json)
    copyfile(
        os.path.join(MODULE_DIR, "network.tf.json"),
        os.path.join(env_dir, "network.tf.json")
    )

    # 2) Genera main.tf.json solo con recursos
    resource_config = {  
        "triggers": {
            "name": env["name"],
            "network": env["network"]
        },
        "provisioner": [{
            "local-exec": {
                "command": f"echo 'Arrancando servidor {env['name']} en red {env['network']}'"
            }
        }]
    }

    config = {
        "resource": [
            {
                "null_resource": [
                    {
                        env["name"]: [resource_config]
                    }
                ]
            }
        ]
    }

    if "depends_on" in env:
        resource_config["depends_on"] = [
            f"null_resource.{dep}" for dep in env["depends_on"]
        ]



    with open(os.path.join(env_dir, "main.tf.json"), "w") as fp:
        json.dump(config, fp, sort_keys=True, indent=4)

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    for env in ENVS:
        render_and_write(env)
    print(f"Generados {len(ENVS)} entornos en '{OUT_DIR}/'")
