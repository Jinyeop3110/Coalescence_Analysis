-- Map LaTeX color spans to Word character styles defined in the reference DOCX.

local function normalized_style(style)
  if not style then
    return ""
  end
  return style:lower():gsub("%s+", "")
end

local function map_style(style)
  local s = normalized_style(style)
  if s:find("color:red", 1, true)
      or s:find("color:#ff0000", 1, true)
      or s:find("color:rgb%(255,0,0%)", 1, false) then
    return "RevisionRed"
  end
  if s:find("color:manuscripteditred", 1, true)
      or s:find("color:#960000", 1, true)
      or s:find("color:rgb%(150,0,0%)", 1, false) then
    return "ManuscriptEditRed"
  end
  if s:find("color:reviewerskyblue", 1, true)
      or s:find("color:#0096dc", 1, true)
      or s:find("color:rgb%(0,150,220%)", 1, false) then
    return "ReviewerBlue"
  end
  if s:find("color:statusgray", 1, true)
      or s:find("color:#5a5a5a", 1, true)
      or s:find("color:rgb%(90,90,90%)", 1, false) then
    return "StatusGray"
  end
  return nil
end

function Span(span)
  local custom_style = map_style(span.attributes["style"])
  if custom_style then
    span.attributes["custom-style"] = custom_style
    span.attributes["style"] = nil
    return span
  end
end
