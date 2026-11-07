#import "template.typ": *

#show: book.with(
  title: "Reading the Wall",
  author: "Edited by Simon Gray; written by Claude (Anthropic)",
)

// ------------------------------------------------------------ front matter

#set page(numbering: "i")
#include "chapters/00-front.typ"

// ------------------------------------------------------------ main matter

#part("Part I", subtitle: "Foundations: how movement works and\u{a0}how\u{a0}to\u{a0}read\u{a0}a\u{a0}problem")
#set page(numbering: "1")
#counter(page).update(1)
#include "chapters/01-movement.typ"
#include "chapters/02-reading.typ"

#part("Part II", subtitle: "The techniques, by\u{a0}category\u{a0}and\u{a0}grade")
#include "chapters/03-feet.typ"
#include "chapters/04-body.typ"
#include "chapters/05-hands.typ"
#include "chapters/06-dynamic.typ"
#include "chapters/07-terrain.typ"

#part("Part III", subtitle: "Grade by grade: what to focus on from VB to V8+")
#include "chapters/08-grades.typ"

#part("Part IV", subtitle: "Your body and how you learn")
#include "chapters/09-considerations.typ"

#part("Appendices")
#include "chapters/10-appendices.typ"
