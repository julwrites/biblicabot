package app

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/julwrites/BotPlatform/pkg/def"
	"github.com/julwrites/ScriptureBot/pkg/utils"
	"golang.org/x/net/html"
)

func GetDesiringGodHtml() *html.Node {
	query := "http://rss.desiringgod.org"

	res, _ := http.Get(query)
	buf := new(bytes.Buffer)
	buf.ReadFrom(res.Body)
	newStr := buf.String()

	fmt.Printf(newStr)

	return utils.QueryHtml(query)
}

func GetDesiringGodArticles() []def.Option {
	var options []def.Option

	doc := GetDesiringGodHtml()

	itemNodes := utils.FilterTree(doc, func(node *html.Node) bool {
		return node.Data == "item"
	})

	for _, node := range itemNodes {
		titleNode := utils.FindNode(node, func(node *html.Node) bool {
			return node.Data == "title"
		})
		linkNode := utils.FindNode(node, func(node *html.Node) bool {
			return strings.Contains(node.Data, "http://rss.desiringgod.org/")
		})

		label := titleNode.FirstChild.Data
		link := linkNode.Data

		log.Printf("Label: %s, Link: %s", label, link)

		if len(label) > 0 && len(link) > 0 {
			options = append(options, def.Option{Text: label, Link: link})
		}
	}

	return options
}
