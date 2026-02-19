## AI Project ##

** setup pre Windows OS **
* spustenie Docker Desktop
* inštalácia K3d (light version for K8s) in PowerShell
winget install k3d
winget install Kubernetes.kubectl
* install python 3.11 version + start in venv cez python lancher
cd project_dir
py -3.11 -m venv .venv
./.venv/Sript/Activate
* spustenie cluster s 2 nodemi a load balancerom 
k3d cluster create ml-lab
k3d cluster create ml-lab --agents 2 --port "8080:80@loadbalancer"
k3d cluster list

* natrenovanie modelu IRIS a uloženie do model store
python train_and_save.py

* preverenie ci je model ulozeny
bentoml models list


### MODEL ###
Ako to funguje v praxi (Oddelenie váh od kódu)

V tvojom prípade už k oddeleniu dochádza, len si to možno neuvedomuješ, pretože sa to deje na tvojom disku:

    **Model Store (Váhy):** Keď spustíš bentoml.sklearn.save_model(), BentoML vezme tie čisté váhy (binárny súbor) a uloží ich do špeciálneho priečinka vo tvojom počítači (zvyčajne v ~/bentoml/models/). Každá verzia má svoj unikátny tag (napr. housing_regressor:abc123xyz).

    **Service Code (Logika):** Tvoj service.py neobsahuje žiadne váhy. Obsahuje len inštrukciu: "Choď do Model Store a vytiahni si odtiaľ najnovšiu verziu modelu s názvom housing_regressor".

**NOTE-PRODUCTION SCENARIO**
V tvojom súčasnom lokálnom setup-e je "úložiskom váh" tvoj disk. Ak by si však pracoval v tíme:

    Váhy by sa ukladali do S3 (AWS), Google Cloud Storage alebo BentoCloud.

    Tvoj Kubernetes cluster by si pri štarte kontajnera stiahol tieto váhy z tohto cloudu.

### NEXT STEP ###
Tvoj ďalší krok v k3d

Keď urobíš bentoml build, BentoML vykoná "magické spojenie":

    *Zoberie tvoj kód (service.py).

    *Zoberie špecifickú verziu váh z tvojho lokálneho Model Store.

    *Zabalí ich spolu do jedného Docker obrazu (tzv. Bento).

Týmto máš zaručené, že ten konkrétny kontajner má v sebe presne tie váhy, s ktorými bol otestovaný.


*spustenie service
bentoml serve service.py:IrisService

*vytvorenie bentofile.yaml

Teraz premeníme tvoj kód a model na jeden balík (Bento) a následne na Docker image. Spusti tieto príkazy v termináli:
*bentoml build
Čo by sa stalo bez build?
Musel by si manuálne písať Dockerfile, riešiť, ako do kontajnera dostať tie binárne váhy modelu, a dávať si pozor, aby si nezabudol na nejakú knižnicu. BentoML to urobil za teba jedným príkazom.

*bentoml containerize iris_classifier:latest


###Nasadenie do k3d (Kubernetes)###

Aby tvoj lokálny Kubernetes videl tento image, musíme ho tam "vložiť", pretože k3d nepoužíva tvoj lokálny Docker registry automaticky.

*import image to cluster
k3d image import iris_classifier:latest -c ml-lab
*run model in kubernetes
kubectl run iris-app --image=iris_classifier:3un6pmimi6a7hyep --port=3000 --image-pull-policy=Never
*expose port 
kubectl port-forward pod/iris-app 3000:3000


## MONITORING##
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
NOTES:
kube-prometheus-stack has been installed. Check its status by running:
  kubectl --namespace default get pods -l "release=monitoring"

Get Grafana 'admin' user password by running:

  kubectl --namespace default get secrets monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo

  pre win
  $secret = kubectl get secret monitoring-grafana -o jsonpath="{.data.admin-password}" 
  [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($secret))


Access Grafana local instance:

  export POD_NAME=$(kubectl --namespace default get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=monitoring" -oname)
  kubectl --namespace default port-forward $POD_NAME 3000

Get your grafana admin user password by running:

  kubectl get secret --namespace default -l app.kubernetes.io/component=admin-secret -o jsonpath="{.items[0].data.admin-password}" | base64 --decode ; echo


  #Spustenie port-forward
  Start-Job -ScriptBlock { kubectl --namespace default port-forward monitoring-grafana-66c64d84c6-zglhw 3000:3000 }
  #zastavenie
  Get-Job
  Stop-Job -Name Job1  # Alebo použi ID, ktoré uvidíš v Get-Job



  ----------------------------------------------------------------

  Toto je kľúčová strategická otázka pre tvoju kariéru. Ak sa chceš stať AI Platform Engineerom, odpoveď nie je „jedno alebo druhé“, ale pochopenie ich poradia v produkčnom reťazci.

Tu je rozbor toho, kam investovať čas podľa tvojich cieľov:
1. BentoML: Tvoj „Operačný systém“ pre modely

BentoML by mal byť tvojím východiskovým bodom. Prečo? Pretože rieši logiku okolo modelu (tzv. "The Last Mile").

    Čo sa naučíš: Ako vytvoriť API, ako riešiť monitoring (Prometheus), ako baliť kontajnery a ako orchestratovať pody v Kubernetes.

    Kedy ho použiť: Vždy, keď potrebuješ nasadiť klasické modely (ako Iris, XGBoost, Scikit-learn) alebo keď tvoj model vyžaduje zložitý Python kód pred/po samotnom výpočte (preprocessing).

2. vLLM a Triton: „Motory“ pre extrémny výkon

Tieto nástroje sú špecializované komponenty, ktoré v profesionálnom prostredí často bežia pod BentoML alebo namiesto jeho Runnerov.

    vLLM: Je to kráľ dnešnej doby pre LLM (Llama, Mistral). Ak chceš pracovať vo firme, ktorá buduje vlastné chatboty, vLLM je dôležitejšie než Triton, pretože rieši špecifické problémy pamäte u veľkých modelov (PagedAttention).

    NVIDIA Triton: Je to priemyselný štandard pre všetko ostatné na GPU (počítačové videnie, audio, video). Je to najkomplexnejší nástroj, ktorý ti dáva najväčšiu kontrolu nad hardvérom.

Čo sa učiť a kedy? (Tvoj plán rozvoja)

Ak chceš pracovať „profesionálnejšie“, postupuj v týchto vlnách:
🌊 Vlna 1: Ovládnutie platformy (BentoML + k3s)

    Prečo: Tu sa naučíš Kubernetes architektúru (pody, služby, ingress, monitorovanie). Bez týchto základov ti bude Triton na nič, lebo ho nebudeš vedieť v klastri ani spustiť.

    Tvoj cieľ: Vedieť nasadiť model, ktorý sa sám škáluje a má funkčné grafy v Grafane.

🌊 Vlna 2: Špecializácia na LLM (vLLM)

    Prečo: LLM sú aktuálne najžiadanejšie.

    Tvoj cieľ: Integrovať vLLM do BentoML (ako Runner). Naučíš sa, ako ušetriť firme tisíce eur optimalizáciou GPU pamäte.

🌊 Vlna 3: Hardvérový Expert (Triton)

    Prečo: Triton je pre fajnšmekrov. Je to dopytované v medicínskom videní, autonómnych autách alebo tam, kde záleží na každej milisekunde.

    Tvoj cieľ: Naučiť sa písať config.pbtxt a optimalizovať modely cez TensorRT.

Verdikt

Ak teraz riešiš Iris a k3d, zostaň hlbšie pri BentoML. Práve na ňom sa naučíš "špinavú prácu" inžiniera (K8s YAML súbory, Docker siete, monitoring), ktorá je univerzálna pre všetky tri technológie.

Keď budeš v k3d suverénne ovládať Deploymenty a ServiceMonitory, prechod na vLLM alebo Triton bude pre teba len výmena „jednej súčiastky v stroji“.

Chcel by si, aby som ti ukázal, ako v tvojom existujúcom BentoML kóde vymeniť ten klasický Runner za vLLM Runner, aby si videl ten rozdiel v praxi?


-------------------------------------------------------------------------------------------------------


System validated with LOCUST at 500 concurrent users, maintaining <150ms latency through adaptive batching.

Pri zmene nastaveni BentoML pouzit pristup GitOps (nainstalovat ArgoCD)

## ARGOCD ##
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

#musia nabehnut sluzby
kubectl get pods -w -n argocd

#start UI
Start-Job -ScriptBlock{kubectl port-forward svc/argocd-server -n argocd 8080:443}

#obtain password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | ForEach-Object { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_)) }
