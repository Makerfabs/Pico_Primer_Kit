# From github:  https://github.com/jeroenhuijzer/SGP30-micropython
import time

SGP30_PRODUCT_TYPE = 0
SGP30_I2C_ADDRESS = 0x58

# command and constants for reading the serial ID
SGP30_CMD_GET_SERIAL_ID = 0x3682
SGP30_CMD_GET_SERIAL_ID_DURATION_US = 500
SGP30_CMD_GET_SERIAL_ID_WORDS = 3

# command and constants for reading the featureset version
SGP30_CMD_GET_FEATURESET = 0x202f
SGP30_CMD_GET_FEATURESET_DURATION_US = 10000
SGP30_CMD_GET_FEATURESET_WORDS = 1

# command and constants for on-chip self-test
SGP30_CMD_MEASURE_TEST = 0x2032
SGP30_CMD_MEASURE_TEST_DURATION_US = 220000
SGP30_CMD_MEASURE_TEST_WORDS = 1
SGP30_CMD_MEASURE_TEST_OK = 0xd400

# command and constants for IAQ init
SGP30_CMD_IAQ_INIT = 0x2003
SGP30_CMD_IAQ_INIT_DURATION_US = 10000

# command and constants for IAQ measure
SGP30_CMD_IAQ_MEASURE = 0x2008
SGP30_CMD_IAQ_MEASURE_DURATION_US = 12000
SGP30_CMD_IAQ_MEASURE_WORDS = 2

# command and constants for getting IAQ baseline
SGP30_CMD_GET_IAQ_BASELINE = 0x2015
SGP30_CMD_GET_IAQ_BASELINE_DURATION_US = 10000
SGP30_CMD_GET_IAQ_BASELINE_WORDS = 2

# command and constants for setting IAQ baseline
SGP30_CMD_SET_IAQ_BASELINE = 0x201e
SGP30_CMD_SET_IAQ_BASELINE_DURATION_US = 10000

# command and constants for raw measure
SGP30_CMD_RAW_MEASURE = 0x2050
SGP30_CMD_RAW_MEASURE_DURATION_US = 25000
SGP30_CMD_RAW_MEASURE_WORDS = 2

# command and constants for setting absolute humidity
SGP30_CMD_SET_ABSOLUTE_HUMIDITY = 0x2061
SGP30_CMD_SET_ABSOLUTE_HUMIDITY_DURATION_US = 10000

# command and constants for getting TVOC inceptive baseline
SGP30_CMD_GET_TVOC_INCEPTIVE_BASELINE = 0x20b3
SGP30_CMD_GET_TVOC_INCEPTIVE_BASELINE_DURATION_US = 10000
SGP30_CMD_GET_TVOC_INCEPTIVE_BASELINE_WORDS = 1

# command and constants for setting TVOC baseline
SGP30_CMD_SET_TVOC_BASELINE = 0x2077
SGP30_CMD_SET_TVOC_BASELINE_DURATION_US = 10000

CRC8_POLYNOMIAL = 0x31
CRC8_INIT = 0xFF
CRC8_LEN = 1

WORD_SIZE = 2


class SGP30:

    def __init__(self, i2c):
        self.i2c = i2c

    def sgp30_check_featureset(self, needed_fs):
        fs_version, product_type = self.sgp30_get_feature_set_version()

        if product_type != SGP30_PRODUCT_TYPE:
            raise RuntimeError("SGP30_ERR_INVALID_PRODUCT_TYPE")

        if fs_version < needed_fs:
            raise RuntimeError("SGP30_ERR_UNSUPPORTED_FEATURE_SET")

    def sgp30_measure_test(self):
        test_result = self.i2c_delayed_read_cmd(SGP30_CMD_MEASURE_TEST,
                                                SGP30_CMD_MEASURE_TEST_DURATION_US,
                                                SGP30_CMD_MEASURE_TEST_WORDS)
        return test_result[0] == SGP30_CMD_MEASURE_TEST_OK

    def sgp30_measure_iaq(self):
        return self.i2c_write_command(SGP30_CMD_IAQ_MEASURE)

    def sgp30_read_iaq(self):
        words = self.i2c_read_words(SGP30_CMD_IAQ_MEASURE_WORDS)
        tvoc_ppb = words[1]
        co2_eq_ppm = words[0]
        return tvoc_ppb, co2_eq_ppm

    def sgp30_measure_iaq_blocking_read(self):
        self.sgp30_measure_iaq()
        time.sleep_us(SGP30_CMD_IAQ_MEASURE_DURATION_US)
        return self.sgp30_read_iaq()

    def sgp30_measure_tvoc(self):
        return self.sgp30_measure_iaq()

    def sgp30_read_tvoc(self):
        tvoc_ppb, _ = self.sgp30_read_iaq()
        return tvoc_ppb

    def sgp30_measure_tvoc_blocking_read(self):
        tvoc_ppb, _ = self.sgp30_measure_iaq_blocking_read()
        return tvoc_ppb

    def sgp30_measure_co2_eq(self):
        return self.sgp30_measure_iaq()

    def sgp30_read_co2_eq(self):
        _, co2_eq_ppm = self.sgp30_read_iaq()
        return co2_eq_ppm

    def sgp30_measure_co2_eq_blocking_read(self):
        _, co2_eq_ppm = self.sgp30_measure_iaq_blocking_read()
        return co2_eq_ppm

    def sgp30_measure_raw_blocking_read(self):
        self.sgp30_measure_raw()
        time.sleep_us(SGP30_CMD_RAW_MEASURE_DURATION_US)
        return self.sgp30_read_raw()

    def sgp30_measure_raw(self):
        return self.i2c_write_command(SGP30_CMD_RAW_MEASURE)

    def sgp30_read_raw(self):
        words = self.i2c_read_words(SGP30_CMD_RAW_MEASURE_WORDS)
        ethanol_raw_signal = words[1]
        h2_raw_signal = words[0]
        return ethanol_raw_signal, h2_raw_signal

    def sgp30_get_iaq_baseline(self):
        self.i2c_write_command(SGP30_CMD_GET_IAQ_BASELINE)
        time.sleep_us(SGP30_CMD_GET_IAQ_BASELINE_DURATION_US)
        words = self.i2c_read_words(SGP30_CMD_GET_IAQ_BASELINE_WORDS)
        baseline = (words[1] << 16) | words[0]
        if not baseline:
            raise RuntimeError("FAILURE GETTING IAQ BASELINE")
        return baseline

    def sgp30_set_iaq_baseline(self, baseline):
        if not baseline:
            raise RuntimeError("FAILURE SETTING IAQ BASELINE")
        words = [(baseline & 0xffff0000) >> 16, baseline & 0x0000ffff]
        self.i2c_write_cmd_with_args(SGP30_CMD_SET_IAQ_BASELINE, words)
        time.sleep_us(SGP30_CMD_SET_IAQ_BASELINE_DURATION_US)

    def sgp30_get_tvoc_inceptive_baseline(self):
        self.sgp30_check_featureset(0x21)
        self.i2c_write_command(SGP30_CMD_GET_TVOC_INCEPTIVE_BASELINE)
        time.sleep_us(SGP30_CMD_GET_TVOC_INCEPTIVE_BASELINE_DURATION_US)
        return self.i2c_read_words(SGP30_CMD_GET_TVOC_INCEPTIVE_BASELINE_WORDS)[0]

    def sgp30_set_tvoc_baseline(self, tvoc_baseline):
        self.sgp30_check_featureset(0x21)
        if not tvoc_baseline:
            raise RuntimeError("FAILURE SETTING TVOC BASELINE")
        self.i2c_write_cmd_with_args(SGP30_CMD_SET_TVOC_BASELINE, [tvoc_baseline])
        time.sleep_us(SGP30_CMD_SET_TVOC_BASELINE_DURATION_US)

    def sgp30_set_absolute_humidity(self, absolute_humidity):
        if absolute_humidity > 256000:
            raise RuntimeError("FAILURE SETTING ABSOLUTE HUMIDITY")
        ah_scaled = (absolute_humidity * 16777) >> 16
        self.i2c_write_cmd_with_args(SGP30_CMD_SET_ABSOLUTE_HUMIDITY, [ah_scaled])
        time.sleep_us(SGP30_CMD_SET_ABSOLUTE_HUMIDITY_DURATION_US)

    def sgp30_get_feature_set_version(self):
        words = self.i2c_delayed_read_cmd(SGP30_CMD_GET_FEATURESET,
                                          SGP30_CMD_GET_FEATURESET_DURATION_US,
                                          SGP30_CMD_GET_FEATURESET_WORDS)
        feature_set_version = words[0] & 0x00FF
        product_type = (words[0] & 0xF000) >> 12
        return feature_set_version, product_type

    def sgp30_get_serial_id(self):
        words = self.i2c_delayed_read_cmd(SGP30_CMD_GET_SERIAL_ID,
                                          SGP30_CMD_GET_SERIAL_ID_DURATION_US,
                                          SGP30_CMD_GET_SERIAL_ID_WORDS)
        serial_id = (words[0] << 32) | (words[1] << 16) | (words[2] << 0)
        return serial_id

    def sgp30_iaq_init(self):
        self.i2c_write_command(SGP30_CMD_IAQ_INIT)
        time.sleep_us(SGP30_CMD_IAQ_INIT_DURATION_US)

    def sgp30_probe(self):
        self.sgp30_check_featureset(0x20)
        return self.sgp30_iaq_init()

    def i2c_read_words_as_bytes(self, num_words):
        size = num_words * (WORD_SIZE + CRC8_LEN)
        buf = bytearray(size)
        self.i2c.readfrom_into(SGP30_I2C_ADDRESS, buf)
        data = []
        for i in range(0, size, WORD_SIZE + CRC8_LEN):
            word_bytes = [buf[i], buf[i + 1]]
            check_crc(word_bytes, buf[i + WORD_SIZE])
            data.append(word_bytes)
        return data

    def i2c_read_words(self, num_words):
        data = self.i2c_read_words_as_bytes(num_words)
        data_words = []
        for word_bytes in data:
            data_words.append((word_bytes[0] << 8) | word_bytes[1])
        return data_words

    def i2c_write_command(self, command):
        buf = fill_cmd_send_buf(command)
        return self.i2c.writeto(SGP30_I2C_ADDRESS, buf)

    def i2c_write_cmd_with_args(self, command, data_words):
        buf = fill_cmd_send_buf(command, data_words)
        return self.i2c.writeto(SGP30_I2C_ADDRESS, buf)

    def i2c_delayed_read_cmd(self, cmd, delay_us, num_words):
        buf = fill_cmd_send_buf(cmd)
        self.i2c.writeto(SGP30_I2C_ADDRESS, buf)
        if delay_us:
            time.sleep_us(delay_us)
        return self.i2c_read_words(num_words)


def fill_cmd_send_buf(cmd, args=None):
    if args is None:
        args = []
    buf = [(cmd & 0xFF00) >> 8, (cmd & 0x00FF) >> 0]
    for arg in args:
        arr = [(arg & 0xFF00) >> 8, (arg & 0x00FF) >> 0]
        arr.append(generate_crc(arr))
        buf += arr
    return bytes(buf)


def generate_crc(data):
    """"calculates 8-Bit checksum with given polynomial"""
    crc = CRC8_INIT
    for current_byte in data:
        crc ^= current_byte
        for crc_bit in range(8, 0, -1):
            if crc & 0x80:
                crc = (crc << 1) ^ CRC8_POLYNOMIAL
            else:
                crc = (crc << 1)
    return crc & CRC8_INIT


def check_crc(data, checksum):
    if generate_crc(data) != checksum:
        raise RuntimeError("CRC Checksum mismatch")
