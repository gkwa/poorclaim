README.md: sect1 sect2 sect3
	cat sect1 >README.md
	cat sect2 >>README.md
	cat sect3 >>README.md

manual.org: main.py data.yaml template.org
	python $<

sect1: header.txt
	cat $< >$@

sect2: manual.org gh-md-toc
	cat $< | ./gh-md-toc - >$@

sect3: manual.org
	docker run --rm --volume "$$(pwd):/data" --user $$(id -u):$$(id -g) pandoc/extra $< --to=gfm --from=org --output=$@

gh-md-toc:
	curl https://raw.githubusercontent.com/ekalinin/github-markdown-toc/master/gh-md-toc -o $@ && chmod +x $@

.PHONY: clean
clean:
	rm -f sect1
	rm -f sect2
	rm -f sect3
