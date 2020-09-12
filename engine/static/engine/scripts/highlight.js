let url = decodeURI(location.href)
const keyword = url.match('keyword=(.*)&?')[1]
const contents = document.querySelectorAll(".hl-able")
const replacement = "<span class='highlight'>" + keyword + "</span>"

// Highlight
for(let i = 0; i< contents.length; ++i){
        const content = contents[i]
        let str = content.innerHTML
        str = str.split(keyword).join(replacement)
        content.innerHTML = str
}
