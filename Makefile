
.PHONY: all clean vidserver vidupdate nodeget cleaner nginxget nginx \
	nginxrun nginxstop nginxreload nginxquit socat nginxenableautoindex

ROOT=$(CURDIR)
DATA=/data/media/vids
REALDATA ?= /data/media/0/realdata
THIRD_PARTY=$(ROOT)/thirdparty

socatlink=http://www.dest-unreach.org/socat/download/socat-1.7.4.4.tar.gz
socattgz=$(THIRD_PARTY)/socat-1.7.4.4.tar.gz
socatdir=$(THIRD_PARTY)/socat-1.7.4.4
socatexe=$(THIRD_PARTY)/socat-1.7.4.4/socat
socatbin=$(THIRD_PARTY)/socat-1.7.4.4/bin/socat
nginxenableautoindexreplaced=$(nginxconf)/.enableautoindex
nginxautoindexconf=$(etcdir)/autoindex.conf
nginxlink=https://nginx.org/download/nginx-1.22.1.tar.gz
nginxtgz=$(THIRD_PARTY)/nginx-1.22.1.tar.gz
nginxdir=$(THIRD_PARTY)/nginx-1.22.1
nginxexe=$(nginxdir)/objs/nginx
nginxrtmplink=https://github.com/arut/nginx-rtmp-module
nodejslink=https://nodejs.org/dist/v19.2.0/node-v19.2.0-linux-arm64.tar.xz
npm_cache=/data/media/.npm
nodejstxz=$(THIRD_PARTY)/node-v19.2.0-linux-arm64.tar.xz
nodejsdir=$(THIRD_PARTY)/node-v19.2.0-linux-arm64
webfstgz=$(THIRD_PARTY)/webfs-1.21.tar.gz
webfsdir=$(THIRD_PARTY)/webfs-1.21/
webfs=$(webfsdir)/webfsd
etcdir=$(ROOT)/etc
nginxconf=$(etcdir)/nginx

all: $(webfs) $(DATA)

$(socatexe):$(socattgz)
	(cd $(THIRD_PARTY); tar -xf $(socattgz))
	(cd $(socatdir); ./configure; make -j2;)

$(socatbin):$(socatexe)
	(cd $(socatdir); mkdir -p bin; cp socat bin)

socat:$(socatbin)
$(socattgz):
	(cd $(THIRD_PARTY); wget $(socatlink))

$(nginxdir):
	(cd $(THIRD_PARTY); wget $(nginxlink))
	(cd $(THIRD_PARTY); tar -xf $(nginxtgz))
	$(RM) $(nginxtgz)
nginxget:$(nginxdir)
	(cd $(nginxdir); git clone $(nginxrtmplink))
$(nginxexe):
	(cd $(nginxdir); ./configure --with-http_ssl_module --with-http_v2_module --with-stream=dynamic --with-http_addition_module --with-http_mp4_module --add-module=nginx-rtmp-module; make -j2; mkdir -p logs)
$(nginxconf):$(nginxexe)
	cp -r $(nginxdir)/conf $(nginxconf)

nginx:$(nginxdir) $(nginxexe) $(nginxconf)

nginxopts := -p $(nginxdir) -c $(etcdir)/nginx/nginx.conf
$(nginxenableautoindexreplaced):
	cp $(nginxautoindexconf) $(nginxconf)/nginx.conf
	touch $(nginxenableautoindexreplaced)
nginxenableautoindex: $(nginxenableautoindexreplaced)
nginxrun:
	sudo $(nginxexe) $(nginxopts)
nginxstop:
	sudo $(nginxexe) $(nginxopts) -s quit
nginxquit:
	sudo $(nginxexe) $(nginxopts) -s quit
nginxreload:
	sudo $(nginxexe) $(nginxopts) -s reload

$(nodejsdir):
	(cd $(THIRD_PARTY); wget $(nodejslink))
	(cd $(THIRD_PARTY); tar -xf $(nodejstxz))
	$(RM) $(nodejstxz)
nodeget:$(nodejsdir)

$(DATA):
	mkdir -p $(DATA)

$(webfsdir):$(webfstgz)
	tar -xzf $(webfstgz) -C $(THIRD_PARTY)

$(webfs):$(webfsdir)
	echo ok
	make -C $(webfsdir) config
	bash -c 'sed -iE '"'"'s/^-e \(LIB.*\)$$/\1/'"'"' $(webfsdir)/Make.config'
	make -C $(webfsdir)

routes := $(shell bash -c "source $(ROOT)/env.sh >/dev/null 2>&1 ; lsroute $(REALDATA)")
vidupdate:
	for route in $(routes); do \
		for i in e d f; do \
			bash -c "source $(ROOT)/env.sh; cd $(DATA); camconcat $(REALDATA) $$route $$i"; \
		done \
	done

vidserver:$(webfs) $(DATA)
	sudo $(webfs) -4 -F -p 80 -r $(DATA)

clean:
	$(RM) -r $(webfsdir)
	$(RM) $(nodejstxz)
	$(RM) -r $(nodejsdir)
	$(RM) $(nginxtgz)
	$(RM) -r $(nginxdir)
	$(RM) $(socattgz)
	$(RM) -r $(socatdir)
	$(RM) -r $(nginxconf)

cleaner: clean
	$(RM) -r $(DATA)
	$(RM) -r $(npm_cache)
