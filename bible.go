// Brief: Scripture API
// Primary responsibility: Query calls for Scripture functionality

package main

import (
	"fmt"
	"log"
	"strings"

	bmul "github.com/julwrites/BotMultiplexer"
	"golang.org/x/net/html"
)

var passageQuery string = "http://www.biblegateway.com/passage/?search=%s&version=%s"

func Query(ref string, env *bmul.SessionData) *html.Node {
	query := fmt.Sprintf(passageQuery, ref, GetUserConfig(&env.User).Version)

	log.Printf("Query String: %s", query)

	doc := GetHtml(query)

	if doc == nil {
		log.Fatalf("Error getting html")
		return nil
	}

	return doc
}

func GetReference(doc *html.Node, env *bmul.SessionData) string {
	refNode, err := FindByClass(doc, "bcv")
	if err != nil {
		log.Fatalf("Error parsing for reference: %v", err)
		return ""
	}

	return refNode.FirstChild.Data
}

func GetPassage(doc *html.Node, env *bmul.SessionData) string {
	passageNode, startErr := FindByClass(doc, "passage-text")
	if startErr != nil {
		log.Fatalf("Error parsing for passage: %v", startErr)
		return ""
	}

	var candNodes []*html.Node
	for child := passageNode.FirstChild; child != nil; child = child.NextSibling {
		candNodes = append(candNodes, child)
	}
	filtNodes := FilterNodeList(candNodes, func(node *html.Node) bool {
		for _, attr := range node.Attr {
			if attr.Key == "class" && attr.Val == "footnotes" {
				return false
			}
		}
		return true
	})

	var textNodes []*html.Node
	for _, node := range filtNodes {
		for _, textNode := range FilterNode(node, func(node *html.Node) bool {
			return node.Type == html.TextNode
		}) {
			textNodes = append(textNodes, textNode)
		}
	}

	var passage strings.Builder

	for _, node := range textNodes {
		passage.WriteString(node.Data)
	}

	return fmt.Sprintf("I currently can't parse a passage but here's what I got so far: %s", passage.String())
}

func GetBiblePassage(env *bmul.SessionData) {
	if len(env.Msg.Message) > 0 {

		doc := Query(env.Msg.Message, env)
		ref := GetReference(doc, env)

		if len(ref) > 0 {
			env.Res.Message = GetPassage(doc, env)
		}
	}
}
