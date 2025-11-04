-- Format Python code in Quarto using isort + Black
-- This Lua filter finds all code blocks with language "python" (or "py").
-- It first runs isort (to sort imports), then Black (for formatting).
-- You can disable per block via attributes {isort=false} and/or {black=false}.

local function is_python_block(cb)
  -- determine whether the block is Python
  for _, cls in ipairs(cb.classes) do
    if cls == "python" or cls == "py" then
      return true
    end
  end
  return false
end

function CodeBlock(cb)
  if not is_python_block(cb) then
    return nil
  end

  -- defaults: both enabled; can be disabled per block
  local attrs = cb.attributes or {}
  local do_isort = attrs["isort"] ~= "false"
  local do_black = attrs["black"] ~= "false"

  -- if both are disabled, do nothing
  if not do_isort and not do_black then
    return nil
  end

  local code = cb.text

  -- 1) isort (if enabled): reads from stdin ("-") and writes to stdout
  -- use the "black" profile for compatibility with Black
  if do_isort then
    local ok_isort, sorted_code = pcall(function()
      return pandoc.pipe("isort", {"-", "--profile", "black", "--stdout"}, code)
    end)
    if ok_isort and type(sorted_code) == "string" and #sorted_code > 0 then
      code = sorted_code
    end
  -- if isort fails, continue with the original code
  end

  -- 2) Black (if enabled): reads from stdin ("-") and returns on stdout
  -- --quiet: no chatter; --fast: faster (skips safety checks)
  if do_black then
    local ok_black, formatted = pcall(function()
      return pandoc.pipe("black", {"-", "--quiet", "--fast"}, code)
    end)

  -- if Black fails, keep at least the isort result (or the original code)
    if ok_black and type(formatted) == "string" and #formatted > 0 then
      code = formatted
    end
  end

  cb.text = code
  return cb
end
