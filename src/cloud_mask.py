def cloud_mask(image):
  qa = image.select('QA60');

  #Bits 10 and 11 are clouds and cirrus, respectively.
  cloudBitMask = 1 << 10;
  cirrusBitMask = 1 << 11;

  # Both flags should be set to zero, indicating clear conditions.
  mask = (qa.bitwiseAnd(cloudBitMask).eq(0)).And(qa.bitwiseAnd(cirrusBitMask).eq(0));

  return image.updateMask(mask)\
              .divide(10000)\
              .copyProperties(image, ["system:time_start"]);
