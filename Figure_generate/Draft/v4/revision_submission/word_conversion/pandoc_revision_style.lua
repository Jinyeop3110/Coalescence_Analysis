-- Map red LaTeX revision spans, produced from \rev{...}, to a Word character
-- style that is defined in the reference DOCX.

local function is_red_style(style)
  if not style then
    return false
  end
  local normalized = style:lower():gsub("%s+", "")
  return normalized:find("color:red", 1, true)
    or normalized:find("color:#ff0000", 1, true)
    or normalized:find("color:rgb%(255,0,0%)", 1, false)
end

function Span(span)
  if is_red_style(span.attributes["style"]) then
    span.attributes["custom-style"] = "RevisionRed"
    span.attributes["style"] = nil
    return span
  end
end
