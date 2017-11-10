// Namespace for this file.
gbGrowingProgressItem = {};

/** Creates the element. */
gbGrowingProgressItem.create = function() {
  console.log('Creating growing progress item.');

  Polymer({
    is: 'gb-growing-progress-item',

    // The total number of days that this plant has to grow for.
    totalDays_: 0,
    // The total number of days that this plant has been growing for.
    elapsedDays_: 0,

    setName: gbGrowingProgressItem.setName_,
    setTotalDays: gbGrowingProgressItem.setTotalDays_,
    setElapsedDays: gbGrowingProgressItem.setElapsedDays_,
    setIcon: gbGrowingProgressItem.setIcon_,

    updateProgressBar_: gbGrowingProgressItem.updateProgressBar_,
  });
};

/** Updates the progress bar.
 * @private
 */
gbGrowingProgressItem.updateProgressBar_ = function() {
  this.$.progress.max = this.totalDays_;
  this.$.progress.value = this.elapsedDays_;

  // Set the description based on the time remaining.
  const remaining = this.totalDays_ - this.elapsedDays_;
  const description = remaining + ' days remaining';
  this.$.daysRemaining.textContent = description;
};

/** Sets the name of the plant.
 * @param name The plant name to set.
 */
gbGrowingProgressItem.setName_ = function(name) {
  this.$.name.textContent = name;
};

/** Sets the total number of days the plant has to grow for.
 * @param days The number of days.
 */
gbGrowingProgressItem.setTotalDays_ = function(days) {
  this.totalDays_ = days;
  this.updateProgressBar_();
};

/** Sets the number of days that this plant has been growing.
 * @param days The number of days.
 */
gbGrowingProgressItem.setElapsedDays_ = function(days) {
  this.elapsedDays_ = days;
  this.updateProgressBar_();
};

/** Sets the icon for the plant.
 * @param iconURL The URL of the icon.
 */
gbGrowingProgressItem.setIcon_ = function(iconURL) {
  this.$.icon.src = iconURL;
};
