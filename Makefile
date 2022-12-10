
.PHONY: all clean vidserver

ROOT=$(CURDIR)
DATA=$(ROOT)/data
THIRD_PARTY=$(ROOT)/thirdparty

webfstgz=$(THIRD_PARTY)/webfs-1.21.tar.gz
webfsdir=$(THIRD_PARTY)/webfs-1.21/
webfs=$(webfsdir)/webfsd

all: $(webfs)

$(webfsdir):$(webfstgz)
	tar -xzf $(webfstgz) -C $(THIRD_PARTY)
$(webfs):$(webfsdir)
	echo ok
	make -C $(webfsdir) config
	bash -c 'sed -iE '"'"'s/^-e \(LIB.*\)$$/\1/'"'"' $(webfsdir)/Make.config'
	make -C $(webfsdir)

vidserver:$(webfs)
	$(webfs) -h

clean:
	$(RM) -r $(webfsdir)
