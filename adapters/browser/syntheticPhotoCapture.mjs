/**
 * Browser image preparation adapted from AlimangoStudio/papps
 * frontend/cms-vue/src/lib/photoCapture.js (generic shrinkTarget / jpegName ideas).
 *
 * This standalone open-source research variant ONLY accepts synthetic fixtures.
 * It always redraws pixels into a new JPEG (never passes through the original),
 * so source file EXIF/device/location metadata is not copied to the output.
 * This is not proof that input pixels contain no identifying information.
 */
export const MAX_EDGE = 2048
export const MAX_PIXELS = 40_000_000
const SUPPORTED_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp'])

export function shrinkTarget(width, height, maxEdge = MAX_EDGE) {
  if (!Number.isFinite(width) || !Number.isFinite(height) || width < 1 || height < 1 ||
      !Number.isFinite(maxEdge) || maxEdge < 1) {
    throw new RangeError('Invalid image dimensions')
  }
  if (width * height > MAX_PIXELS) throw new RangeError('Image exceeds synthetic test pixel limit')
  const scale = Math.min(1, maxEdge / Math.max(width, height))
  return { width: Math.max(1, Math.round(width * scale)), height: Math.max(1, Math.round(height * scale)) }
}

export function jpegName(name) {
  const safe = String(name || 'synthetic').replace(/[^a-zA-Z0-9_.-]/g, '_')
  const base = safe.replace(/\.[^./\\]+$/, '') || 'synthetic'
  return `${base}.jpg`
}

/** Explicit local-only demo; refuse if synthetic status was not asserted. */
export async function prepareSyntheticImage(file, { synthetic = false, maxEdge = MAX_EDGE, quality = 0.85 } = {}) {
  if (synthetic !== true) throw new Error('Synthetic fixture opt-in required; never process patient images')
  if (!file || !SUPPORTED_TYPES.has(file.type)) throw new Error('Unsupported synthetic image')
  if (typeof document === 'undefined' || typeof Image === 'undefined') throw new Error('Requires a browser canvas')
  if (typeof URL === 'undefined' || typeof URL.createObjectURL !== 'function') throw new Error('Requires local object URLs')
  if (!Number.isFinite(quality) || quality < 0.1 || quality > 1) throw new RangeError('Invalid JPEG quality')
  const url = URL.createObjectURL(file)
  try {
    const img = await new Promise((resolve, reject) => {
      const image = new Image()
      image.onload = () => resolve(image)
      image.onerror = () => reject(new Error('Could not decode synthetic image'))
      image.src = url
    })
    const { width, height } = shrinkTarget(img.naturalWidth, img.naturalHeight, maxEdge)
    const canvas = document.createElement('canvas')
    canvas.width = width
    canvas.height = height
    const ctx = canvas.getContext('2d')
    if (!ctx) throw new Error('No 2D drawing context')
    ctx.drawImage(img, 0, 0, width, height)
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', quality))
    if (!blob) throw new Error('Re-encoding failed; original was not returned')
    return new File([blob], jpegName(file.name), { type: 'image/jpeg' })
  } finally {
    URL.revokeObjectURL(url)
  }
}
