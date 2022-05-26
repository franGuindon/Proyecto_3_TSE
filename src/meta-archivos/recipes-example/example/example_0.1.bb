#SUMMARY = "My test videos"
#DESCRIPTION = "Test Videos"
#HOMEPAGE = ""
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI = "file://Detector_de_emociones.py \ 
	   file://model.tflite \
	   file://model_optimized.tflite \
	   file://haarcascade_frontalface_default.xml "

S = "${WORKDIR}"

TARGET_CC_ARCH += "${LDFLAGS}"

#FILES_${PN} += "${libdir}/*"
#FILES_${PN}-dev = "${libdir}/* ${includedir}"


do_install () {
   install -d ${D}${bindir}/DETECTOR
   install -m 0755 Detector_de_emociones.py ${D}${bindir}/DETECTOR
   install -m 0755 model.tflite ${D}${bindir}/DETECTOR
   install -m 0755 model_optimized.tflite ${D}${bindir}/DETECTOR
   install -m 0755 haarcascade_frontalface_default.xml ${D}${bindir}/DETECTOR
}

