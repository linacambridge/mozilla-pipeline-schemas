import json, os, unittest
from jsonschema import validate, ValidationError

LOCAL = os.path.dirname(__file__)
SAMPLE_PING_PATH = os.path.join(LOCAL, 'sample_v4_ping.json')
MAIN_SCHEMA_PATH = os.path.join(LOCAL, '../../telemetry/main.schema.json')

BAD_LOCALES = [ # Actually seen in 1st 15 months of UT release
    "e.-US", "http", "enmUS", "`g",
    "TelemetryController::_sampleForOptoutTelemetry - sampling for optout Telemetry - offset: 42",
    "range: 5", "sample: 18", "esmAR", "esmDS", "en%US", "es,AR",
    "application/vnd.rn-realaudio", "x86", "locale", "added", "https:",
    "narrow", "zh-C",
    "C:\Users\home\AppData\Roaming\Mozilla\Firefox\Profiles\lnc8jzsz.default\saved-telemetry-pings85a6c99-8535-4a0b-ab99-87b8fb464117",
    "pt,BR", "eswES", "t2", "pt-B", "release", "x-test"]

GOOD_LOCALES = [
    "ja-JP-osaka", "ltg", "roa-ES-val", "ca-valencia",
    # to here uncommon but valid corner cases; below here most common
    "id", "hu", "tr", "nl", "es-MX", "ja", "en-GB", "it", "zh-CN",
    "pl", "pt-BR", "ru", "es-ES", "fr", "de", "en-US"
]

class Test_validate(unittest.TestCase):

    def setUp(self):
        with open(SAMPLE_PING_PATH) as f:
            self.ping = json.load(f)

    def test_main(self):
        with open(MAIN_SCHEMA_PATH) as f:
            main_schema = json.load(f)
        # The presence of $schema means that validate() will test
        # for specific JSON-Schema features
        self.failUnless("$schema" in main_schema)
        # Sanity
        self.failUnless("properties" in main_schema)
        self.failUnless("required" in main_schema)
        self.assertRaises(ValidationError, validate, {}, main_schema)
        validate(self.ping, main_schema)

        self.ping['creationDate'] = self.ping['creationDate'][:1]
        self.assertRaises(ValidationError, validate, self.ping, main_schema)

    def test_locale(self):
        with open(MAIN_SCHEMA_PATH) as f:
            main_schema = json.load(f)
        self.ping['environment']['settings']['locale'] = 1
        self.assertRaises(ValidationError, validate, self.ping, main_schema)
        for locale in BAD_LOCALES:
            self.ping['environment']['settings']['locale'] = locale
            self.assertRaises(ValidationError, validate,
                              self.ping, main_schema)
        for locale in GOOD_LOCALES:
            self.ping['environment']['settings']['locale'] = locale
            validate(self.ping, main_schema)


if __name__ == '__main__':
    unittest.main()
