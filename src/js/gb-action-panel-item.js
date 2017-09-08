// Namespace for this file.
gbActionPanelItem = {};

/** Creates the element. */
gbActionPanelItem.create = function() {
  console.log('Creating panel item element.');

  Polymer({
    is: 'gb-action-panel-item',

    // The level of the item.
    level_: null,

    getTitle: gbActionPanelItem.getTitle_,
    getDescription: gbActionPanelItem.getDescription_,
    getLevel: gbActionPanelItem.getLevel_,

    setTitle: gbActionPanelItem.setTitle_,
    setDescription: gbActionPanelItem.setDescription_,
    setLevel: gbActionPanelItem.setLevel_,
  });
};

/** Maps icons to their source urls.
 */
gbActionPanelItem.ICON_URLS = {normal: "../images/icon_check.svg",
                               warning: "../images/icon_warning.svg",
                               error: "../images/icon_error.svg"}

/** Gets the title of the action panel item.
 * @returns The title of the item. */
gbActionPanelItem.getTitle_ = function() {
  return this.$.title.textContent;
};

/** Gets the description of the action panel item.
 * @returns The description of the item. */
gbActionPanelItem.getDescription_ = function() {
  return this.$.description.textContent;
};

/** Gets the level of the action panel item.
 * @returns The level of the item. */
gbActionPanelItem.getLevel_ = function() {
  return this.level_;
};

/** Sets the title of the action panel item.
 * @param title The title to set.
 */
gbActionPanelItem.setTitle_ = function(title) {
  this.$.title.textContent = title;
};

/** Sets the description of the action panel item.
 * @param description The description to set.
 */
gbActionPanelItem.setDescription_ = function(description) {
  this.$.description.textContent = description;
};

/** Sets the level of the action panel item, which will change its placement, as
 * well as the icon next to it.
 * @param level A string in "normal", "warning", or "error".
 */
gbActionPanelItem.setLevel_ = function(level) {
  // Set the icon correctly.
  this.$.icon.src = gbActionPanelItem.ICON_URLS[level];
  this.level_ = level;
};
