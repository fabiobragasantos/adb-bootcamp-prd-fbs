# Databricks notebook source
# MAGIC %md # Mount Point

# COMMAND ----------

# MAGIC %md
# MAGIC ### Vinculando o Key Vault ao Databricks
# MAGIC   * Para criar o escopo: url_do_seu_databeicks#secrets/createScope
# MAGIC   * https://learn.microsoft.com/pt-br/azure/databricks/security/secrets/secret-scopes

# COMMAND ----------

# MAGIC %md ### Criando conexão com o adls

# COMMAND ----------

# MAGIC %md #### Mountpoint simples

# COMMAND ----------

scopo-kv-bootcamp-prd-fbs

# COMMAND ----------

dbutils.fs.mount(
    source = "wasbs://delta@dlsbootcampprdfbs.blob.core.windows.net"
    ,mount_point = "/mnt/delta/"
    ,extra_configs = {"fs.azure.account.key.dlsbootcampprdfbs.blob.core.windows.net" :dbutils.secrets.get(scope = "scopo-kv-bootcamp-prd-fbs", key = "secret-dlsbootcampprdfbs")}
)

# COMMAND ----------

# MAGIC %fs ls "/mnt/delta"

# COMMAND ----------

dbutils.fs.unmount( f"/mnt/delta/")

# COMMAND ----------

# MAGIC %fs ls "/mnt/delta"

# COMMAND ----------

# MAGIC %md #### Mountpoint com boas praticas

# COMMAND ----------

config =  {"fs.azure.account.key.dlsbootcampprdfbs.blob.core.windows.net" :dbutils.secrets.get(scope = "scopo-kv-bootcamp-prd-fbs", key = "secret-dlsbootcampprdfbs")}

# COMMAND ----------

# DBTITLE 1,Lista de diretórios do lake 
#apenas os diretórios que vamos interagir
diretorios = ['raw','transient','delta']

# COMMAND ----------

# DBTITLE 1,Criando o mountpoint entre o lake e o databricks
def mount_diretorio_lake(lst_diretorios):
    try:        
        for diretorio in lst_diretorios:
            dbutils.fs.mount(
                source = f"wasbs://{diretorio}@dlsbootcampprdfbs.blob.core.windows.net"
                ,mount_point = f"/mnt/{diretorio}/"
                ,extra_configs = config
            )
            print(f"{diretorio} = ok")
            
    except ValueError as error:
        print(error)
        
mount_diretorio_lake(diretorios)        

# COMMAND ----------

# DBTITLE 1,Desmontando as conexões com o lake
def unmount_diretorio_lake(lst_diretorios):
    try:
        for diretorio in lst_diretorios:
            dbutils.fs.unmount( f"/mnt/{diretorio}/")
            print(f"{diretorio} = ok")
            
    except ValueError as error:
        print(error)
        
unmount_diretorio_lake(diretorios)   

# COMMAND ----------

# DBTITLE 1,listando diretórios no DBFS com o dbutils
dbutils.fs.ls("/mnt/raw/apis/instrutores/")

# COMMAND ----------

# MAGIC %fs ls "/mnt/raw/apis/instrutores/"
