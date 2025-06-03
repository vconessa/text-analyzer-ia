const express = require('express');
const router = express.Router();

const { analyzeText } = require('../controllers/analyzeController');

// POST /analyze
router.post('/', analyzeText);

module.exports = router;
