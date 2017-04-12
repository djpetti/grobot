// Namespace for this file.
gbActionPanelItem = {};

/** Creates the element. */
gbActionPanelItem.create = function() {
  Polymer({
    is: 'gb-action-panel-item',
    behaviors: [main.getReduxBehavior()],

    setTitle: gbActionPanelItem.setTitle,
    setDescription: gbActionPanelItem.setDescription,
    setLevel: gbActionPanelItem.setLevel,
  });
};

/** Maps icons to their source urls.
 * @private
 */
ICON_URLS_ = {normal: "../images/icon_check.svg",
              warning: "../images/icon_warning.svg",
              error: "../images/icon_error.svg"}

/** Sets the title of the action panel item.
 * @param title The title to set.
 */
gbActionPanelItem.setTitle = function(title) {
  this.$.title.textContent = title;
};

/** Sets the description of the action panel item.
 * @param description The description to set.
 */
gbActionPanelItem.setDescription = function(description) {
  this.$.description.textContent = description;
};

/** Sets the level of the action panel item, which will change its placement, as
 * well as the icon next to it.
 * @param level A string in "normal", "warning", or "error".
 */
gbActionPanelItem.setLevel = function(level) {
  // Set the icon correctly.
  this.$.icon.src = ICON_URLS_[level];
};
