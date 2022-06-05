#SUMMARY = "My test videos"
#DESCRIPTION = "Test Videos"
#HOMEPAGE = ""
LICENSE = "CLOSED"
LIC_FILES_CHKSUM = ""

SRC_URI = "file://arg_parser.py \
	   file://detect.tflite \
      file://main.py \
      file://obj_classifier.py \
	   file://gpio.py "

S = "${WORKDIR}"

TARGET_CC_ARCH += "${LDFLAGS}"

#FILES_${PN} += "${libdir}/*"
#FILES_${PN}-dev = "${libdir}/* ${includedir}"


do_install () {
   install -d ${D}${bindir}/BANDA
   install -m 0755 arg_parser.py ${D}${bindir}/BANDA
   install -m 0755 detect.tflite ${D}${bindir}/BANDA
   install -m 0755 main.py ${D}${bindir}/BANDA
   install -m 0755 obj_classifier.py ${D}${bindir}/BANDA
   install -m 0755 gpio.py ${D}${bindir}/BANDA
}

