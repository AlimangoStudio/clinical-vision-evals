import test from 'node:test'
import assert from 'node:assert/strict'
import { MAX_EDGE, jpegName, shrinkTarget, prepareSyntheticImage } from '../../adapters/browser/syntheticPhotoCapture.mjs'

test('bounds long edge without enlarging', () => {
  assert.deepEqual(shrinkTarget(6000, 3000), {width: MAX_EDGE, height: 1024})
  assert.deepEqual(shrinkTarget(400, 200), {width: 400, height: 200})
})
test('rejects impossible or oversized dimensions', () => {
  assert.throws(() => shrinkTarget(0, 2), RangeError)
  assert.throws(() => shrinkTarget(10000, 10000), RangeError)
})
test('normalizes synthetic file names', () => {
  assert.equal(jpegName('a photo.png'), 'a_photo.jpg')
  assert.equal(jpegName('image'), 'image.jpg')
})
test('rejects patient-like inputs without explicit synthetic opt-in', async () => {
  await assert.rejects(() => prepareSyntheticImage({type: 'image/jpeg', name: 'sample.jpg'}), /Synthetic fixture opt-in/)
})
