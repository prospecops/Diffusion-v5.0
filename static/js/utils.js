// utils.js

function darken(hexColor, percent) {
  // First, check if the hex color is valid and then remove the hash sign
  const sanitizedHexColor = hexColor.startsWith('#') ? hexColor.slice(1) : hexColor;

  // Parse the hex color
  const num = parseInt(sanitizedHexColor, 16);
  const amt = Math.round(2.55 * percent);

  // Apply the darken effect
  const R = (num >> 16) - amt;
  const B = (num >> 8 & 0x00FF) - amt;
  const G = (num & 0x0000FF) - amt;

  // Reconstruct the hex color and return it
  return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 + (B < 255 ? B < 1 ? 0 : B : 255) * 0x100 + (G < 255 ? G < 1 ? 0 : G : 255)).toString(16).slice(1);
}
