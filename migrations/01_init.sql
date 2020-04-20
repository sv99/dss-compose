--
-- Up
--

SET FOREIGN_KEY_CHECKS = 0;
ALTER DATABASE `DSS` DEFAULT CHARACTER SET 'utf8';
-- ----------------------------
-- Table structure for problem
-- ----------------------------
CREATE TABLE problem (
    problem_id INTEGER NOT NULL AUTO_INCREMENT,
    description TEXT NOT NULL,
    created_at TIMESTAMP,
    PRIMARY KEY (problem_id));

-- ----------------------------
-- Table structure for recommendation
-- ----------------------------
CREATE TABLE recommendation (
    recommendation_id INTEGER NOT NULL AUTO_INCREMENT,
    recommendation TEXT NOT NULL,
    created_at TIMESTAMP,
    PRIMARY KEY (recommendation_id));

-- ----------------------------
-- Table structure for problem_recommendation
-- ----------------------------
CREATE TABLE problem_recommendation (
    problem_id INTEGER NOT NULL,
    recommendation_id INTEGER NOT NULL,
    rating INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (problem_id, recommendation_id),
    FOREIGN KEY (problem_id) REFERENCES problem (problem_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (recommendation_id) REFERENCES recommendation (recommendation_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE);

SET FOREIGN_KEY_CHECKS = 1;

--
-- Down
--
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS problem_recommendation;
DROP TABLE IF EXISTS recommendation;
DROP TABLE IF EXISTS problem;
SET FOREIGN_KEY_CHECKS = 1;
