
# backupy baz

## setup
- wszystkie nasze bazy są uruchomione na kontenerach dockera
- docker jest "enginem" który działa na jakimś hoście; aby działać z backupami trzeba się na niego zalogować (ssh)
- potem znaleźć ID kontenera (1sza kolumna z `docker ps`) (wystarczą pierwsze 3 znaki ID'ka, np. `77a`)
- wszystkie nasze kontenery baz mają zrobiony "docker volume"; tzn. np. folder `/home/ubuntu/db/backups`
  jest podłączony do foldera `/backups` wewnątrz kontenera
- aby działać z backupami, najlepiej wlogować się do kontenera `docker exec -it {ID} bash`, gdzie ID to ID kontenera ↑↑

## komendy/programy do backup-u

### tworzenie backupów
```
docker exec -it {ID} bash
su postgres
cd /backups         #powinna mieć prawa zapisu dla usera postgres
pg_dump {nazwa_bazy} {opcje} > {nazwa pliku}

# np: pg_dump postgres --schema=s9999movies > backup-$(date +%Y%m%d-T%H:%M:%S).sql
```

### przywracanie stanu bazy
```
docker exec -it {ID} bash
su postgres
cd /backups         
psql -f backup_17.sql {nazwa_bazy}
```
