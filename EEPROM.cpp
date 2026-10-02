#include "EEPROM.h"
#include <hardware/flash.h>
#include <hardware/sync.h>

// Allocate space at the end of RP2040 flash (last 4KB sector)
// RP2040 default flash size is typically 2MB (0x200000)
#ifndef FLASH_SECTOR_SIZE
#define FLASH_SECTOR_SIZE 4096
#endif

#ifndef PICO_FLASH_SIZE_BYTES
#define PICO_FLASH_SIZE_BYTES (2 * 1024 * 1024)
#endif

static const uint32_t EEPROM_FLASH_OFFSET = (PICO_FLASH_SIZE_BYTES - FLASH_SECTOR_SIZE);

EEPROMClass::EEPROMClass() : _buffer(NULL), _size(0), _dirty(false) {}

EEPROMClass::~EEPROMClass() {
    end();
}

void EEPROMClass::begin(size_t size) {
    if (size == 0) return;
    if (size > FLASH_SECTOR_SIZE) size = FLASH_SECTOR_SIZE;

    if (_buffer) {
        delete[] _buffer;
    }

    _size = size;
    _buffer = new uint8_t[_size];
    _dirty = false;

    // Read flash content into RAM buffer
    const uint8_t *flash_ptr = (const uint8_t *)(XIP_BASE + EEPROM_FLASH_OFFSET);
    for (size_t i = 0; i < _size; i++) {
        _buffer[i] = flash_ptr[i];
    }
}

uint8_t EEPROMClass::read(int idx) {
    if (!_buffer || idx < 0 || (size_t)idx >= _size) return 0;
    return _buffer[idx];
}

void EEPROMClass::write(int idx, uint8_t val) {
    if (!_buffer || idx < 0 || (size_t)idx >= _size) return;
    if (_buffer[idx] != val) {
        _buffer[idx] = val;
        _dirty = true;
    }
}

bool EEPROMClass::commit() {
    if (!_buffer || !_dirty) return true;

    // Prepare a full sector buffer for flash programming
    uint8_t sector_buf[FLASH_SECTOR_SIZE];
    const uint8_t *flash_ptr = (const uint8_t *)(XIP_BASE + EEPROM_FLASH_OFFSET);

    // Copy flash content into sector buffer
    for (size_t i = 0; i < FLASH_SECTOR_SIZE; i++) {
        sector_buf[i] = (i < _size) ? _buffer[i] : flash_ptr[i];
    }

    // Disable interrupts while erasing and programming flash
    uint32_t ints = save_and_disable_interrupts();
    flash_range_erase(EEPROM_FLASH_OFFSET, FLASH_SECTOR_SIZE);
    flash_range_program(EEPROM_FLASH_OFFSET, sector_buf, FLASH_SECTOR_SIZE);
    restore_interrupts(ints);

    _dirty = false;
    return true;
}

void EEPROMClass::end() {
    if (_buffer) {
        delete[] _buffer;
        _buffer = NULL;
    }
    _size = 0;
    _dirty = false;
}

uint8_t& EEPROMClass::operator[](int idx) {
    static uint8_t dummy = 0;
    if (!_buffer || idx < 0 || (size_t)idx >= _size) return dummy;
    return _buffer[idx];
}

EEPROMClass EEPROM;
